def to_simple_markdown(title, body):
    return f"""## {title}\n\n{body}"""


def rules_to_list_section(title, rules):
    per_rule = """* {RULE}\n > {EXPLANATION}"""

    rules_formatted_list = []

    for rule in rules:
        rule_formatted = per_rule.format(RULE=rule.rule, EXPLANATION=rule.explanation)
        rules_formatted_list.append(rule_formatted)

    rules_formatted = "\n".join(rules_formatted_list)
    final_formatted = f"## {title}\n\n{rules_formatted}"
    return final_formatted
