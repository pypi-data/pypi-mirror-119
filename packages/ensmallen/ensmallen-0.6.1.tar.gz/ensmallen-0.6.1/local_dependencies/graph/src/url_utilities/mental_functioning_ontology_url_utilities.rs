use super::*;

#[automatically_generated_function]
/// Returns whether the given node name respects the Mental Functioning Ontology nodes pattern.
///
/// # Arguments
/// * `node_name`: &str - Node name to check pattern with.
///
/// # Example
/// To validate a node you can use:
/// ```rust
/// # use graph::*;
/// let this_library_node_name = "MF:0000013";
/// let not_this_library_node_name = "PizzaQuattroStagioni";
/// assert!(is_valid_mental_functioning_ontology_node_name(this_library_node_name));
/// assert!(!is_valid_mental_functioning_ontology_node_name(not_this_library_node_name));
/// ```
pub fn is_valid_mental_functioning_ontology_node_name(node_name: &str) -> bool {
    is_valid_node_name_from_seeds(
        node_name,
        Some(&["MF"]),
        Some(10),
        Some(":"),
        None,
        Some(7),
        Some(7),
    )
    .is_ok()
}

#[automatically_generated_function]
/// Returns URL from given Mental Functioning Ontology node name.
///
/// # Arguments
/// * `node_name`: &str - Node name to check pattern with.
///
/// # Safety
/// This method assumes that the provided node name is a Mental Functioning Ontology node name and
/// may cause a panic if the aforementioned assumption is not true.
///
pub(crate) unsafe fn format_mental_functioning_ontology_url_from_node_name(
    node_name: &str,
) -> String {
    format_url_from_node_name(
        "http://purl.obolibrary.org/obo/MF_{node_name}",
        node_name,
        Some(":"),
    )
}
