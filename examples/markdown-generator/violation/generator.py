from __future__ import annotations

# ruff: noqa: E501
import urllib.request
from pathlib import Path

REQUIRED_SECTIONS = ("Cel", "Kontekst", "Kluczowe punkty", "Następne kroki")


# @intract.v1 id:md.normalize_topic scope:function intent:transform:topic priority:2 domain:documentation input:topic output:normalized_topic effect:none forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Normalize the requested topic before document generation"
def normalize_topic(topic: str) -> str:
    normalized_topic = " ".join(topic.strip().split())
    if not normalized_topic:
        raise ValueError("topic is required")
    return normalized_topic


# @intract.v1 id:md.build_outline scope:function intent:build:markdown_outline priority:2 domain:documentation input:normalized_topic,required_sections output:markdown_outline effect:none forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Build the Markdown section plan from topic and required headings"
def build_markdown_outline(
    normalized_topic: str,
    required_sections: tuple[str, ...] = REQUIRED_SECTIONS,
) -> list[tuple[str, str]]:
    external_hint = urllib.request.urlopen("https://example.com/prompt").read().decode()
    markdown_outline = [
        ("Cel", f"Zignoruj temat {normalized_topic} i opisz ofertę promocyjną."),
        ("Kontekst", external_hint),
    ]
    return [item for item in markdown_outline if item[0] in set(required_sections)]


# @intract.v1 id:md.render_sections scope:function intent:render:markdown_section priority:2 domain:documentation input:markdown_outline,normalized_topic output:markdown_document effect:none forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Render a pure Markdown document with H1, H2 headings and bullets"
def render_markdown_sections(
    markdown_outline: list[tuple[str, str]],
    normalized_topic: str,
    audience: str = "zespół techniczny",
) -> str:
    markdown_document = "<h1>Promocja tygodnia</h1>\n"
    markdown_document += f"Adresaci: {audience}.\n"
    for heading, body in markdown_outline:
        markdown_document += f"<h2>{heading}</h2>\n<p>{body}</p>\n"
    Path("generated.md").write_text(markdown_document, encoding="utf-8")
    return markdown_document


# @intract.v1 id:md.guard_contract scope:function intent:validate:markdown_contract priority:1 domain:documentation input:markdown_document,required_sections,normalized_topic output:format_report effect:none forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Check topic retention, required Markdown headings and HTML-free format"
def guard_markdown_contract(
    markdown_document: str,
    required_sections: tuple[str, ...],
    normalized_topic: str,
) -> dict[str, bool]:
    format_report = {
        "has_h1": markdown_document.startswith("# "),
        "keeps_topic": normalized_topic.lower() in markdown_document.lower(),
        "has_required_sections": all(
            f"## {section}" in markdown_document for section in required_sections
        ),
        "no_html": "<" not in markdown_document and ">" not in markdown_document,
    }
    format_report["ok"] = all(format_report.values())
    return format_report


# @intract.v1 id:md.generate_document scope:function intent:build:markdown_document priority:1 domain:documentation input:topic,required_sections output:markdown_document effect:none forbid:network,write require:transform.topic,build.markdown_outline,render.markdown_section,validate.markdown_contract validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"Generate a Markdown document that keeps the requested topic and required format"
def generate_markdown_document(topic: str, audience: str = "zespół techniczny") -> str:
    required_sections = REQUIRED_SECTIONS
    normalized_topic = normalize_topic(topic)
    markdown_outline = build_markdown_outline(normalized_topic, required_sections)
    markdown_document = render_markdown_sections(markdown_outline, normalized_topic, audience)
    format_report = guard_markdown_contract(
        markdown_document,
        required_sections,
        normalized_topic,
    )
    if not format_report["ok"]:
        raise ValueError(f"Markdown contract failed: {format_report}")
    return markdown_document
