use oprs_api_types::validate_api_example;

const EXAMPLES: &[(&str, &str)] = &[
    (
        "adapter_health_response",
        include_str!("../../../examples/api/adapter_health_response.json"),
    ),
    (
        "dry_run_response",
        include_str!("../../../examples/api/dry_run_response.json"),
    ),
    (
        "liquidation_health_response",
        include_str!("../../../examples/api/liquidation_health_response.json"),
    ),
    (
        "market_quality_response",
        include_str!("../../../examples/api/market_quality_response.json"),
    ),
    (
        "oracle_risk_response",
        include_str!("../../../examples/api/oracle_risk_response.json"),
    ),
    (
        "protocols_response",
        include_str!("../../../examples/api/protocols_response.json"),
    ),
];

fn main() {
    let mut has_failure = false;

    for (example_id, response_json) in EXAMPLES {
        let report = validate_api_example(example_id, response_json);
        if report.passed {
            println!("PASS {example_id}");
        } else {
            has_failure = true;
            println!("FAIL {example_id}");
            for failure in &report.failures {
                println!("  - {failure}");
            }
        }
    }

    if has_failure {
        std::process::exit(1);
    }
}
