use oprs_core::{DryRunStatus, RiskReasonCode};
use oprs_replay::{
    validate_fixture_case, validate_fixture_catalog, FixtureContent, FixtureValidationCase,
};

struct Case<'a> {
    fixture_set_id: &'a str,
    manifest_json: &'a str,
    dry_run_output_json: &'a str,
    content_files: &'a [FixtureContent<'a>],
    expected_status: DryRunStatus,
    expected_reason_codes: &'a [RiskReasonCode],
}

const CATALOG: &str = include_str!("../../../datasets/sample/fixture_catalog.json");

const CASES: &[Case<'_>] = &[
    Case {
        fixture_set_id: "drift_synthetic_margin_001",
        manifest_json: include_str!("../../../datasets/sample/drift_synthetic_margin_001/manifest.json"),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_margin_001/dry_run_output.json"
        ),
        content_files: &[
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/README.md",
                bytes: include_bytes!("../../../datasets/sample/drift_synthetic_margin_001/README.md"),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/canonical_event.json",
                bytes: include_bytes!("../../../datasets/sample/drift_synthetic_margin_001/canonical_event.json"),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/dry_run_output.json",
                bytes: include_bytes!("../../../datasets/sample/drift_synthetic_margin_001/dry_run_output.json"),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/oracle_snapshot.json",
                bytes: include_bytes!("../../../datasets/sample/drift_synthetic_margin_001/oracle_snapshot.json"),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/position_snapshot.json",
                bytes: include_bytes!("../../../datasets/sample/drift_synthetic_margin_001/position_snapshot.json"),
            },
            FixtureContent {
                path: "datasets/sample/drift_synthetic_margin_001/publish_gate.json",
                bytes: include_bytes!("../../../datasets/sample/drift_synthetic_margin_001/publish_gate.json"),
            },
        ],
        expected_status: DryRunStatus::Unsupported,
        expected_reason_codes: &[RiskReasonCode::ExecutionDisabledDryRun],
    },
    Case {
        fixture_set_id: "drift_synthetic_stale_oracle_001",
        manifest_json: include_str!(
            "../../../datasets/sample/drift_synthetic_stale_oracle_001/manifest.json"
        ),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json"
        ),
        content_files: &[FixtureContent {
            path: "datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_stale_oracle_001/dry_run_output.json"
            ),
        }],
        expected_status: DryRunStatus::Rejected,
        expected_reason_codes: &[
            RiskReasonCode::StaleOracle,
            RiskReasonCode::ExecutionDisabledDryRun,
        ],
    },
    Case {
        fixture_set_id: "drift_synthetic_wide_confidence_001",
        manifest_json: include_str!(
            "../../../datasets/sample/drift_synthetic_wide_confidence_001/manifest.json"
        ),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_wide_confidence_001/dry_run_output.json"
        ),
        content_files: &[FixtureContent {
            path: "datasets/sample/drift_synthetic_wide_confidence_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_wide_confidence_001/dry_run_output.json"
            ),
        }],
        expected_status: DryRunStatus::Rejected,
        expected_reason_codes: &[
            RiskReasonCode::WideOracleConfidence,
            RiskReasonCode::ExecutionDisabledDryRun,
        ],
    },
    Case {
        fixture_set_id: "drift_synthetic_missing_oracle_001",
        manifest_json: include_str!(
            "../../../datasets/sample/drift_synthetic_missing_oracle_001/manifest.json"
        ),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_missing_oracle_001/dry_run_output.json"
        ),
        content_files: &[FixtureContent {
            path: "datasets/sample/drift_synthetic_missing_oracle_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_missing_oracle_001/dry_run_output.json"
            ),
        }],
        expected_status: DryRunStatus::Rejected,
        expected_reason_codes: &[
            RiskReasonCode::MissingOracle,
            RiskReasonCode::ExecutionDisabledDryRun,
        ],
    },
    Case {
        fixture_set_id: "drift_synthetic_oracle_divergence_001",
        manifest_json: include_str!(
            "../../../datasets/sample/drift_synthetic_oracle_divergence_001/manifest.json"
        ),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_oracle_divergence_001/dry_run_output.json"
        ),
        content_files: &[FixtureContent {
            path: "datasets/sample/drift_synthetic_oracle_divergence_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_oracle_divergence_001/dry_run_output.json"
            ),
        }],
        expected_status: DryRunStatus::Rejected,
        expected_reason_codes: &[
            RiskReasonCode::OracleMarkDivergence,
            RiskReasonCode::ExecutionDisabledDryRun,
        ],
    },
    Case {
        fixture_set_id: "drift_synthetic_adapter_version_mismatch_001",
        manifest_json: include_str!(
            "../../../datasets/sample/drift_synthetic_adapter_version_mismatch_001/manifest.json"
        ),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_adapter_version_mismatch_001/dry_run_output.json"
        ),
        content_files: &[FixtureContent {
            path: "datasets/sample/drift_synthetic_adapter_version_mismatch_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_adapter_version_mismatch_001/dry_run_output.json"
            ),
        }],
        expected_status: DryRunStatus::Rejected,
        expected_reason_codes: &[
            RiskReasonCode::AdapterVersionMismatch,
            RiskReasonCode::ExecutionDisabledDryRun,
        ],
    },
    Case {
        fixture_set_id: "drift_synthetic_guardrail_unknown_pause_bit_001",
        manifest_json: include_str!(
            "../../../datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/manifest.json"
        ),
        dry_run_output_json: include_str!(
            "../../../datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/dry_run_output.json"
        ),
        content_files: &[FixtureContent {
            path: "datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/dry_run_output.json",
            bytes: include_bytes!(
                "../../../datasets/sample/drift_synthetic_guardrail_unknown_pause_bit_001/dry_run_output.json"
            ),
        }],
        expected_status: DryRunStatus::Rejected,
        expected_reason_codes: &[
            RiskReasonCode::DataQualityLow,
            RiskReasonCode::ExecutionDisabledDryRun,
        ],
    },
];

fn main() {
    let fixture_ids = CASES
        .iter()
        .map(|case| case.fixture_set_id)
        .collect::<Vec<_>>();
    let catalog_report = validate_fixture_catalog(CATALOG, &fixture_ids);
    print_report(&catalog_report);

    let mut failed = !catalog_report.passed;
    for case in CASES {
        let report = validate_fixture_case(FixtureValidationCase {
            fixture_set_id: case.fixture_set_id,
            manifest_json: case.manifest_json,
            dry_run_output_json: case.dry_run_output_json,
            content_files: case.content_files,
            expected_status: case.expected_status,
            expected_reason_codes: case.expected_reason_codes,
        });
        failed |= !report.passed;
        print_report(&report);
    }

    if failed {
        std::process::exit(1);
    }
}

fn print_report(report: &oprs_replay::FixtureValidationReport) {
    if report.passed {
        println!("PASS {}", report.fixture_set_id);
    } else {
        println!("FAIL {}", report.fixture_set_id);
        for failure in &report.failures {
            println!("  - {failure}");
        }
    }
}
