// Copyright © 2016 Smana <smainklh@gmail.com>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"
	"os"

	"github.com/smana/kargo/common"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	noClone        bool
	GcePemFile     string
	GceZone        string
	GceImage       string
	GceMasterType  string
	GceNodeType    string
	GceEtcdType    string
	GceProjectID   string
	GceSvcAccEmail string
	GceTags        []string
)

// gceCmd represents the gce command
var gceCmd = &cobra.Command{
	Use:   "gce",
	Short: "Run instances on Google Compute Engine",
	Long:  "",
	Run:   runGCE,
}

func init() {
	RootCmd.AddCommand(gceCmd)
	gceCmd.Flags().BoolVar(&noClone, "noclone", false, "Do not clone the git repo. Useful when the repo is already downloaded")
	gceCmd.Flags().StringVar(&GcePemFile, "pem-file", "", "GCE pem file path")
	gceCmd.Flags().StringVar(&GceZone, "zone", "", "GCE Zone where the machines will be started")
	gceCmd.Flags().StringVar(&GceImage, "image", "", "GCE machine image")
	gceCmd.Flags().StringVar(&GceMasterType, "masters-machine-type", "", "GCE machine type for Masters (default: n1-standard-2)")
	gceCmd.Flags().StringVar(&GceNodeType, "nodes-machine-type", "", "GCE machine type for Nodes (default: n1-standard-4)")
	gceCmd.Flags().StringVar(&GceEtcdType, "etcds-machine-type", "", "GCE machine type for Etcds members (default: n1-standard-1)")
	gceCmd.Flags().StringVar(&GceProjectID, "project", "", "GCE project ID")
	gceCmd.Flags().StringVar(&GceSvcAccEmail, "email", "", "GCE service account email")
	gceCmd.Flags().Uint16Var(&etcdCount, "etcds", 0, "Number of etcd, these instances will just act as etcd members")
	gceCmd.Flags().Uint16Var(&masterCount, "masters", 0, "Number of masters, these instances will not run workloads, master components only")
	gceCmd.Flags().Uint16Var(&nodeCount, "nodes", 0, "Number of worker nodes")
	gceCmd.Flags().StringSliceVar(&GceTags, "tags", []string{}, "List of tags")
}

func runGCE(cmd *cobra.Command, args []string) {
	// Clone Kargo repository
	if !noClone {
		if common.PathExists(viper.GetString("KargoPath")) {
			if !common.AskForConfirmation("Kargo directory exists, do you want to overwrite it ?") {
				fmt.Printf("%s Aborted, not cloning kargo repository \n ", YellowPrint("WARN:"))
				os.Exit(2)
			}
			os.RemoveAll(viper.GetString("KargoPath"))
		}
		fmt.Printf("%s Cloning kargo repository into %s ... \n ", GreenPrint("INFO:"), viper.GetString("KargoPath"))
		common.GitClone("https://github.com/kubespray/kargo", viper.GetString("KargoPath"))
	} else {
		fmt.Printf("%s Kargo repository %s already exists, not cloning it. \n ", YellowPrint("WARN:"), viper.GetString("KargoPath"))
	}
	if nodeCount == 0 {
		cmd.Help()
		Log.Fatal("Option 'nodes' is required. Number of nodes to run")
	}
}
