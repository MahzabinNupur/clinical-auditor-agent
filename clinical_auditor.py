"""Experimental rule-driven clinical auditor.
Not validated for clinical use.
"""

import re


note_headings = {
    "Clinical Note:",
    "Assessment:",
    "Plan:",
    "History:",
    "Findings:",
    "Chief Complaint:"
}


def normalize_clinical_terms(text):
    """
    Normalize selected equivalent clinical expressions.
    This is a small, controlled terminology prototype.
    """
    text = str(text).casefold()

    # Expand the abbreviation BMI
    text = re.sub(
        r"\bbmi\b",
        "body mass index",
        text
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def retrieve_normalized_evidence(concept, sentence_map):
    """
    Find segments containing a clinical concept
    after terminology and whitespace normalization.

    This retrieves candidate evidence only.
    It does not verify polarity or full fact preservation.
    """

    normalized_concept = normalize_clinical_terms(concept)

    # Require phrase boundaries to avoid substring matches
    pattern = (
        r"(?<!\w)"
        + re.escape(normalized_concept)
        + r"(?!\w)"
    )

    matching_ids = []

    for sid, sentence in sentence_map.items():

        normalized_sentence = normalize_clinical_terms(
            sentence
        )

        if re.search(pattern, normalized_sentence):
            matching_ids.append(sid)

    return matching_ids


def detect_negation_with_uncertainty(sentence, concept):
    """
    Experimental detector with uncertainty recognition.

    Returns:
        affirmed
        negated
        uncertain
        not_mentioned
    """

    text = sentence.casefold()
    target = concept.casefold()

    concept_pattern = (
        r"(?<!\w)"
        + re.escape(target)
        + r"(?!\w)"
    )

    # Split contrasting clauses
    clauses = re.split(
        r"\b(?:but|however|although|whereas)\b|[.;]",
        text
    )

    for clause in clauses:

        match = re.search(concept_pattern, clause)

        if match is None:
            continue

        preceding = clause[:match.start()]

        uncertainty_patterns = [
            r"\bdoes not deny\b",
            r"\bdo not deny\b",
            r"\bcannot rule out\b",
            r"\bcan't rule out\b",
            r"\bpossible\b",
            r"\bsuspected\b"
        ]

        if any(
            re.search(pattern, preceding)
            for pattern in uncertainty_patterns
        ):
            return "uncertain"

        negation_patterns = [
            r"\bdenies?\b",
            r"\bno\b",
            r"\bwithout\b",
            r"\bnegative for\b"
        ]

        if any(
            re.search(pattern, preceding)
            for pattern in negation_patterns
        ):
            return "negated"

        return "affirmed"

    return "not_mentioned"


def detect_ambiguous_negation_scope(sentence, concept):
    """
    Flag potentially ambiguous negation scope.

    Returns:
        uncertain
        or the existing detector's classification
    """

    text = sentence.casefold()
    target = concept.casefold()

    # Detect a comma-separated statement beginning with "No"
    # and ending with an affirmative reporting expression.
    ambiguous_pattern = (
        r"\bno\s+[^.;]+,\s*[^.;]+\b"
        r"(?:present|reported|noted)\b"
    )

    if (
        re.search(ambiguous_pattern, text)
        and re.search(
            r"(?<!\w)" + re.escape(target) + r"(?!\w)",
            text
        )
    ):
        return "uncertain"

    return detect_negation_with_uncertainty(
        sentence, concept
    )


def compare_clinical_polarity(source_status, note_status):
    """
    Compare source and generated-note polarity.

    This only evaluates polarity, not complete
    clinical fact preservation.
    """

    valid_statuses = {
        "affirmed",
        "negated",
        "uncertain",
        "not_mentioned"
    }

    if (
        source_status not in valid_statuses
        or note_status not in valid_statuses
    ):
        return "invalid_input"

    if note_status == "not_mentioned":
        return "missing"

    if (
        source_status == "uncertain"
        or note_status == "uncertain"
    ):
        return "requires_review"

    if source_status == "not_mentioned":
        return "requires_review"

    if source_status != note_status:
        return "contradicted"

    return "polarity_preserved"


def audit_clinical_concept(
    concept,
    source_text,
    note_sentence_map
):
    """
    Integrated clinical concept auditor with
    consistent terminology normalization.

    Experimental rule-driven prototype.
    """

    normalized_concept = normalize_clinical_terms(concept)

    # Exclude headings but preserve sentence IDs
    clinical_segments = {
        sid: text
        for sid, text in note_sentence_map.items()
        if text.strip() not in note_headings
    }

    # Normalize source evidence before polarity analysis
    normalized_source = normalize_clinical_terms(source_text)

    source_polarity = detect_negation_scope_v2(
        normalized_source,
        normalized_concept
    )

    # Retrieve candidate note segments
    evidence_ids = retrieve_normalized_evidence(
        concept,
        clinical_segments
    )

    note_polarities = []

    for sid in evidence_ids:
        normalized_sentence = normalize_clinical_terms(
            clinical_segments[sid]
        )

        note_polarities.append(
            detect_negation_scope_v2(
                normalized_sentence,
                normalized_concept
            )
        )

    if not evidence_ids:
        note_polarity = "not_mentioned"
    elif len(set(note_polarities)) == 1:
        note_polarity = note_polarities[0]
    else:
        note_polarity = "uncertain"

    alignment_status = compare_clinical_polarity(
        source_polarity,
        note_polarity
    )

    return {
        "concept": concept,
        "source_polarity": source_polarity,
        "note_polarity": note_polarity,
        "alignment_status": alignment_status,
        "evidence_ids": evidence_ids
    }



def classify_component_preservation(component_results):
    """
    Classify preservation across explicitly required components.
    """

    values = list(component_results.values())

    if all(values):
        return "present"
    elif any(values):
        return "partial"
    else:
        return "missing"


def verify_fact_components(sentence_map, requirements):
    """
    Experimental component-level fact verifier.

    requirements:
        Dictionary mapping component names
        to regular-expression patterns.

    Returns:
        Component matches, evidence IDs,
        and provisional preservation status.

    Limitation:
        Does not verify relationships between
        components or their clinical context.
    """

    component_results = {}
    component_evidence = {}

    for component, pattern in requirements.items():

        matching_ids = [
            sid
            for sid, sentence in sentence_map.items()
            if re.search(pattern, sentence, re.IGNORECASE)
        ]

        component_results[component] = bool(matching_ids)
        component_evidence[component] = matching_ids

    predicted_status = classify_component_preservation(
        component_results
    )

    return {
        "predicted_status": predicted_status,
        "components": component_results,
        "component_evidence": component_evidence
    }


def detect_negation_scope_v2(sentence, concept):
    """
    Experimental clause-aware polarity detector.

    Separates independent findings connected by:
    ', with' and ', without'.

    Preserves the existing detector for other cases.
    """

    normalized_sentence = normalize_clinical_terms(sentence)
    normalized_concept = normalize_clinical_terms(concept)

    # Split only at explicitly marked clause boundaries
    clauses = re.split(
        r",\s+(?=with\b|without\b)",
        normalized_sentence,
        flags=re.IGNORECASE
    )

    # Find the clause containing the clinical concept
    matching_clauses = [
        clause
        for clause in clauses
        if re.search(
            r"(?<!\w)" + re.escape(normalized_concept) + r"(?!\w)",
            clause
        )
    ]

    if not matching_clauses:
        return "not_mentioned"

    # Multiple matches require review instead of guessing
    if len(matching_clauses) > 1:
        return "uncertain"

    return detect_ambiguous_negation_scope(
        matching_clauses[0],
        normalized_concept
    )


def retrieve_equivalent_expressions(sentence_map, expressions):
    """
    Retrieve evidence matching any explicitly supplied
    equivalent clinical expression.

    Expressions are regular-expression patterns.

    This function performs retrieval only.
    It does not establish complete fact preservation.
    """
    evidence_ids = []

    for sid, sentence in sentence_map.items():
        normalized_sentence = normalize_clinical_terms(sentence)

        if any(
            re.search(
                pattern,
                normalized_sentence,
                flags=re.IGNORECASE
            )
            for pattern in expressions
        ):
            evidence_ids.append(sid)

    return evidence_ids


def evidence_supported_gate(
    prediction,
    sentence_map,
    candidate_ids
):
    """
    Validate a clinical preservation prediction
    against available numbered evidence.

    This checks evidence consistency only.
    It does not establish clinical correctness.
    """

    status = prediction.get("status")
    evidence_ids = prediction.get("evidence_ids", [])

    issues = []

    valid_statuses = {
        "present", "partial", "missing", "contradicted"
    }

    if status not in valid_statuses:
        issues.append("invalid_status")

    if not isinstance(evidence_ids, list):
        issues.append("invalid_evidence_format")
        evidence_ids = []

    if len(evidence_ids) != len(set(evidence_ids)):
        issues.append("duplicate_evidence_ids")

    if any(sid not in sentence_map for sid in evidence_ids):
        issues.append("unknown_evidence_ids")

    if status in {"present", "partial", "contradicted"}:
        if not evidence_ids:
            issues.append("missing_supporting_evidence")

    if status == "missing" and evidence_ids:
        issues.append("unexpected_evidence_for_missing")

    # Candidate retrieval is not exhaustive.
    # Flag differences for review, not automatic rejection.
    if evidence_ids and not set(evidence_ids).intersection(
        candidate_ids
    ):
        issues.append("evidence_outside_retrieval_candidates")

    return {
        "prediction": status,
        "evidence_ids": evidence_ids,
        "validation_status": (
            "requires_review" if issues
            else "provisional_evidence_linked"
        ),
        "issues": issues
    }
