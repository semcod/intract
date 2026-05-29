#[derive(Debug, Clone, Default)]
pub struct Contract {
    pub scope: String,
    pub intent: String,
    pub priority: u8,
    pub domain: Option<String>,
    pub input: Vec<String>,
    pub output: Vec<String>,
    pub effect: Vec<String>,
    pub forbid: Vec<String>,
    pub require: Vec<String>,
    pub validate: Vec<String>,
    pub meaning: Option<String>,
}

fn csv(values: &[String]) -> String {
    values.join(",")
}

pub fn inline_contract(contract: &Contract, prefix: &str) -> String {
    let mut parts = vec![
        "@intract.v1".to_string(),
        format!("scope:{}", contract.scope),
        format!("intent:{}", contract.intent),
        format!("priority:{}", if contract.priority == 0 { 3 } else { contract.priority }),
    ];

    if let Some(domain) = &contract.domain {
        parts.push(format!("domain:{}", domain));
    }
    if !contract.input.is_empty() {
        parts.push(format!("input:{}", csv(&contract.input)));
    }
    if !contract.output.is_empty() {
        parts.push(format!("output:{}", csv(&contract.output)));
    }
    if !contract.effect.is_empty() {
        parts.push(format!("effect:{}", csv(&contract.effect)));
    }
    if !contract.forbid.is_empty() {
        parts.push(format!("forbid:{}", csv(&contract.forbid)));
    }
    if !contract.require.is_empty() {
        parts.push(format!("require:{}", csv(&contract.require)));
    }
    if !contract.validate.is_empty() {
        parts.push(format!("validate:{}", csv(&contract.validate)));
    }
    if let Some(meaning) = &contract.meaning {
        parts.push(format!("meaning:\"{}\"", meaning));
    }

    format!("{} {}", prefix, parts.join(" "))
}
