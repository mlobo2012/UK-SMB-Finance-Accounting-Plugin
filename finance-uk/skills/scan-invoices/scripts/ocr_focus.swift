#!/usr/bin/env swift

import AppKit
import Foundation
import Vision

func usage() -> Never {
    fputs("usage: ocr_focus.swift --manifest-path <manifest.json> --output-path <output.json>\n", stderr)
    exit(1)
}

func readText(from imagePath: String) throws -> String {
    let url = URL(fileURLWithPath: imagePath)
    guard let image = NSImage(contentsOf: url) else {
        throw NSError(domain: "ocr_focus", code: 1, userInfo: [NSLocalizedDescriptionKey: "Failed to load image \(imagePath)"])
    }

    var rect = CGRect(origin: .zero, size: image.size)
    guard let cgImage = image.cgImage(forProposedRect: &rect, context: nil, hints: nil) else {
        throw NSError(domain: "ocr_focus", code: 2, userInfo: [NSLocalizedDescriptionKey: "Failed to create CGImage for \(imagePath)"])
    }

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    request.recognitionLanguages = ["en-GB", "en-US"]

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try handler.perform([request])

    let lines = (request.results ?? []).compactMap { observation -> String? in
        observation.topCandidates(1).first?.string
    }
    return lines.joined(separator: "\n")
}

func normaliseLine(_ value: String) -> String {
    value
        .trimmingCharacters(in: .whitespacesAndNewlines)
        .replacingOccurrences(of: "\t", with: " ")
}

func firstMatch(in value: String, pattern: String) -> String? {
    guard let regex = try? NSRegularExpression(pattern: pattern, options: [.caseInsensitive]) else {
        return nil
    }
    let nsValue = value as NSString
    let range = NSRange(location: 0, length: nsValue.length)
    guard let match = regex.firstMatch(in: value, options: [], range: range), match.numberOfRanges > 1 else {
        return nil
    }
    return nsValue.substring(with: match.range(at: 1))
}

func looksLikeInvoiceNumber(_ value: String) -> Bool {
    let compact = value.replacingOccurrences(of: " ", with: "")
    return compact.range(of: #"^(?=.*\d)[A-Z0-9]{6,}$"#, options: .regularExpression) != nil
}

func looksLikeVATNumber(_ value: String) -> Bool {
    let compact = value
        .uppercased()
        .replacingOccurrences(of: " ", with: "")
        .replacingOccurrences(of: "GB", with: "")
    return compact.range(of: #"^\d{9}$"#, options: .regularExpression) != nil
}

func looksLikeDate(_ value: String) -> Bool {
    let compact = value.trimmingCharacters(in: CharacterSet(charactersIn: ": "))
    return compact.range(of: #"^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$"#, options: .regularExpression) != nil
        || compact.range(of: #"^[A-Z][a-z]{2,8}\s+\d{1,2},\s+\d{4}$"#, options: .regularExpression) != nil
}

func extractCandidate(lines: [String], labels: [String], validator: (String) -> Bool) -> String? {
    for (index, rawLine) in lines.enumerated() {
        let line = normaliseLine(rawLine)
        let upperLine = line.uppercased()
        for label in labels where upperLine.contains(label) {
            var candidates: [String] = []
            if let range = upperLine.range(of: label) {
                candidates.append(String(line[range.upperBound...]).trimmingCharacters(in: CharacterSet(charactersIn: ": .")))
            }
            let nextIndex = index + 1
            if nextIndex < lines.count {
                candidates.append(normaliseLine(lines[nextIndex]))
            }

            for candidate in candidates {
                let cleaned = candidate
                    .trimmingCharacters(in: CharacterSet(charactersIn: ": ."))
                    .replacingOccurrences(of: "|", with: " ")
                if validator(cleaned) {
                    return cleaned
                }
            }
        }
    }

    return nil
}

func mergedLines(from texts: [String]) -> [String] {
    texts
        .flatMap { $0.components(separatedBy: .newlines) }
        .map(normaliseLine)
        .filter { !$0.isEmpty }
}

let arguments = CommandLine.arguments
guard let manifestIndex = arguments.firstIndex(of: "--manifest-path"),
      manifestIndex + 1 < arguments.count,
      let outputIndex = arguments.firstIndex(of: "--output-path"),
      outputIndex + 1 < arguments.count else {
    usage()
}

let manifestPath = arguments[manifestIndex + 1]
let outputPath = arguments[outputIndex + 1]

let manifestURL = URL(fileURLWithPath: manifestPath)
let outputURL = URL(fileURLWithPath: outputPath)

guard let data = try? Data(contentsOf: manifestURL),
      let json = try? JSONSerialization.jsonObject(with: data, options: []),
      var items = json as? [[String: Any]] else {
    fputs("Failed to read manifest JSON at \(manifestPath)\n", stderr)
    exit(2)
}

for index in items.indices {
    let headerPath = items[index]["header_crop_path"] as? String
    let footerPath = items[index]["footer_crop_path"] as? String

    var headerText = ""
    var footerText = ""

    if let headerPath {
        headerText = (try? readText(from: headerPath)) ?? ""
    }
    if let footerPath {
        footerText = (try? readText(from: footerPath)) ?? ""
    }

    let lines = mergedLines(from: [headerText, footerText])
    let invoiceCandidate = extractCandidate(
        lines: lines,
        labels: ["INVOICE NO", "INVOICE NO.", "INVOICE NO:"],
        validator: looksLikeInvoiceNumber
    )
    let vatCandidate = extractCandidate(
        lines: lines,
        labels: ["VAT REG NO", "VAT REG.", "VAT #", "VAT:"],
        validator: looksLikeVATNumber
    )
    let dateCandidate = extractCandidate(
        lines: lines,
        labels: ["DATE:"],
        validator: looksLikeDate
    )

    items[index]["header_ocr_text"] = headerText
    items[index]["footer_ocr_text"] = footerText
    items[index]["ocr_invoice_number_candidate"] = invoiceCandidate ?? NSNull()
    items[index]["ocr_supplier_vat_candidate"] = vatCandidate ?? NSNull()
    items[index]["ocr_date_candidate"] = dateCandidate ?? NSNull()
}

let outputData = try JSONSerialization.data(withJSONObject: items, options: [.prettyPrinted])
try outputData.write(to: outputURL)
print("OCR hints written to \(outputPath)")
