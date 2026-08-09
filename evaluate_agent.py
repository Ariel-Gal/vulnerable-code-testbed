#!/usr/bin/env python3
"""Scores a SAST/AI-agent report against benchmark_manifest.json ground truth.

Usage:
    python evaluate_agent.py benchmark_manifest.json appsec_report.json
    python evaluate_agent.py benchmark_manifest.json results.sarif
"""
import argparse
import json
import sys

# A manifest finding counts as "hit" if the report has a finding on the same
# file (normalized, suffix match) within this many lines of start_line.
LINE_TOLERANCE = 3


def normalize_path(path):
    return path.replace("\\", "/").lstrip("./").lower()


def load_manifest(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["items"]


def load_report_findings(path):
    """Returns a list of (file_path, line) tuples from a SARIF file or a
    simple appsec_report.json ({"findings": [{"file_path":..., "line":...}]})."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    findings = []
    if "runs" in data:  # SARIF
        for run in data["runs"]:
            for result in run.get("results", []):
                for loc in result.get("locations", []):
                    phys = loc.get("physicalLocation", {})
                    uri = phys.get("artifactLocation", {}).get("uri", "")
                    line = phys.get("region", {}).get("startLine", 0)
                    findings.append((uri, line))
    else:  # appsec_report.json
        for item in data.get("findings", data.get("items", [])):
            findings.append((
                item.get("file_path") or item.get("file", ""),
                item.get("start_line") or item.get("line", 0),
            ))
    return findings


def matches(manifest_item, findings):
    target = normalize_path(manifest_item["file_path"])
    target_line = manifest_item["start_line"]
    for file_path, line in findings:
        if normalize_path(file_path).endswith(target) or target.endswith(normalize_path(file_path)):
            if abs(int(line or 0) - target_line) <= LINE_TOLERANCE:
                return True
    return False


def evaluate(manifest_items, findings):
    true_positive_items = [i for i in manifest_items if i["type"] == "true_positive"]
    fp_trap_items = [i for i in manifest_items if i["type"] == "false_positive_trap"]

    tp = sum(1 for i in true_positive_items if matches(i, findings))
    fn = len(true_positive_items) - tp
    fp = sum(1 for i in fp_trap_items if matches(i, findings))

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "total_true_positives": len(true_positive_items),
        "total_fp_traps": len(fp_trap_items),
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def print_summary(stats):
    width = 44
    print("+" + "-" * width + "+")
    print("|{:^{w}}|".format("SAST AGENT BENCHMARK RESULTS", w=width))
    print("+" + "-" * width + "+")
    rows = [
        ("True Positives (TP)", f"{stats['tp']} / {stats['total_true_positives']}"),
        ("False Positives (FP)", f"{stats['fp']} / {stats['total_fp_traps']}"),
        ("False Negatives (FN)", str(stats["fn"])),
        ("Precision", f"{stats['precision']:.2%}"),
        ("Recall", f"{stats['recall']:.2%}"),
        ("F1-Score", f"{stats['f1']:.2%}"),
    ]
    for label, value in rows:
        print("| {:<28}{:>14} |".format(label, value))
    print("+" + "-" * width + "+")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to benchmark_manifest.json")
    parser.add_argument("report", help="Path to the agent's SARIF or appsec_report.json")
    args = parser.parse_args()

    manifest_items = load_manifest(args.manifest)
    findings = load_report_findings(args.report)
    stats = evaluate(manifest_items, findings)
    print_summary(stats)


if __name__ == "__main__":
    sys.exit(main())
