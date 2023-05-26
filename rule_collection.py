from utils import convert_to_date, get_relative_date


class Rule:
    """Class for storing rule data."""
    # string related predicate functions
    STRING_RULES_CONDITIONS = {
        "contains": lambda value, field_value: value in field_value,
        "does_not_contain": lambda value, field_value: value not in field_value,
        "equals": lambda value, field_value: value == field_value,
        "does_not_equals": lambda value, field_value: value != field_value,
    }
    # date related predicate functions
    DATE_RULES_CONDITIONS = {
        "less_than": lambda value, field_value: convert_to_date(field_value) > get_relative_date(value),
        "greater_than": lambda value, field_value: convert_to_date(field_value) < get_relative_date(value),
    }
    """ For additional predicates in future, add functions here."""

    def __init__(self, rule):
        try:
            self.field_name = rule['field_name']
            self.predicate = rule['predicate']
            self.value = rule['value']
            self.available_conditions = self.get_type(self.predicate)
        except KeyError as e:
            raise Exception(f"{e.args} is not present in rules")
    
    def get_type(self, predicate):
        """Evaluate type of predicate and assign available conditions"""
        type_of_data = {}
        if self.STRING_RULES_CONDITIONS.get(predicate, None):
            type_of_data = self.STRING_RULES_CONDITIONS
        elif self.DATE_RULES_CONDITIONS.get(predicate, None):
            type_of_data = self.DATE_RULES_CONDITIONS
        return type_of_data

    def verify(self, email_data):
        """Applying rule by calling respective functions."""
        value_from_email = email_data.get(self.field_name)
        try:
            return self.available_conditions[self.predicate](self.value, value_from_email)
        except KeyError as e:
            raise ValueError(f"Invalid predicate value for rule of {self.field_name}")
        


class RuleCollection:
    """Class for storing rule set and actions"""
    PREDICATE_CONDITIONS = {
        "all": lambda email, rules: all(rule.verify(email) for rule in rules),
        "any": lambda email, rules: any(rule.verify(email) for rule in rules)
    }

    def __init__(self, rule_set):
        try:
            self.predicate = rule_set["predicate"]
            self.actions = rule_set["actions"]
            self.rules = [Rule(rule) for rule in rule_set["rules"]]
        except KeyError as e:
            raise Exception(f'{e.args} not present in rules')

    def verify(self, email_data):
        try:
            return self.PREDICATE_CONDITIONS[self.predicate](email_data, self.rules)
        except KeyError as e:
            raise ValueError("Invalid value for rule collection predicate")
