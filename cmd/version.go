package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

func init() {
	RootCmd.AddCommand(versionCmd)
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version number of Kargo",
	Long:  `All software has versions. This is Kargo's`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("0.4.6")
	},
}
