package main

import (
	"fmt"

	intractsdk "github.com/intract/sdk-go/intractsdk"
)

func main() {
	fmt.Println(intractsdk.Inline(intractsdk.Contract{
		Scope:    "function",
		Intent:   "scan:project_files",
		Priority: 1,
		Domain:   "scanner",
		Input:    []string{"sourceTree"},
		Output:   []string{"fileList"},
		Effect:   []string{"read"},
		Forbid:   []string{"network"},
		Validate: []string{"input_presence", "output_presence", "return_value"},
		Meaning:  "collect source files from project tree",
	}, "//"))
}
