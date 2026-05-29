package io.intract.sdk;

import java.util.ArrayList;
import java.util.List;
import java.util.StringJoiner;

public class IntractContract {
    public String scope;
    public String intent;
    public int priority = 3;
    public String domain = "";
    public List<String> input = new ArrayList<>();
    public List<String> output = new ArrayList<>();
    public List<String> effect = new ArrayList<>();
    public List<String> forbid = new ArrayList<>();
    public List<String> require = new ArrayList<>();
    public List<String> validate = new ArrayList<>();
    public String meaning = "";

    public String inline(String prefix) {
        if (prefix == null || prefix.isBlank()) {
            prefix = "//";
        }

        List<String> parts = new ArrayList<>();
        parts.add("@intract.v1");
        parts.add("scope:" + scope);
        parts.add("intent:" + intent);
        parts.add("priority:" + priority);

        if (!domain.isBlank()) parts.add("domain:" + domain);
        if (!input.isEmpty()) parts.add("input:" + join(input));
        if (!output.isEmpty()) parts.add("output:" + join(output));
        if (!effect.isEmpty()) parts.add("effect:" + join(effect));
        if (!forbid.isEmpty()) parts.add("forbid:" + join(forbid));
        if (!require.isEmpty()) parts.add("require:" + join(require));
        if (!validate.isEmpty()) parts.add("validate:" + join(validate));
        if (!meaning.isBlank()) parts.add("meaning:\"" + meaning + "\"");

        return prefix + " " + String.join(" ", parts);
    }

    private String join(List<String> values) {
        StringJoiner joiner = new StringJoiner(",");
        for (String value : values) {
            joiner.add(value);
        }
        return joiner.toString();
    }
}
