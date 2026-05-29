package intractsdk

import (
	"fmt"
	"strings"
)

type Contract struct {
	Scope    string
	Intent   string
	Priority int
	Domain   string
	Input    []string
	Output   []string
	Effect   []string
	Forbid   []string
	Require  []string
	Validate []string
	Meaning  string
}

func csv(values []string) string {
	return strings.Join(values, ",")
}

func Inline(c Contract, prefix string) string {
	if prefix == "" {
		prefix = "//"
	}
	priority := c.Priority
	if priority == 0 {
		priority = 3
	}

	parts := []string{
		"@intract.v1",
		"scope:" + c.Scope,
		"intent:" + c.Intent,
		fmt.Sprintf("priority:%d", priority),
	}

	if c.Domain != "" {
		parts = append(parts, "domain:"+c.Domain)
	}
	if len(c.Input) > 0 {
		parts = append(parts, "input:"+csv(c.Input))
	}
	if len(c.Output) > 0 {
		parts = append(parts, "output:"+csv(c.Output))
	}
	if len(c.Effect) > 0 {
		parts = append(parts, "effect:"+csv(c.Effect))
	}
	if len(c.Forbid) > 0 {
		parts = append(parts, "forbid:"+csv(c.Forbid))
	}
	if len(c.Require) > 0 {
		parts = append(parts, "require:"+csv(c.Require))
	}
	if len(c.Validate) > 0 {
		parts = append(parts, "validate:"+csv(c.Validate))
	}
	if c.Meaning != "" {
		parts = append(parts, fmt.Sprintf("meaning:%q", c.Meaning))
	}

	return prefix + " " + strings.Join(parts, " ")
}
