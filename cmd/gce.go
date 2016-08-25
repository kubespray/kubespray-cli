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

import "github.com/spf13/cobra"

var (
	gcePemFile     string
	gceZone        string
	gceImage       string
	gceMasterType  string
	gceNodeType    string
	gceEtcdType    string
	gceProjectID   string
	gceSvcAccEmail string
	gceTags        []string
)

// gceCmd represents the gce command
var gceCmd = &cobra.Command{
	Use:   "gce",
	Short: "Run instances on Google Compute Engine",
	Long:  "",
	Run:   runHelp,
}

func init() {
	RootCmd.AddCommand(gceCmd)
	gceCmd.Flags().StringVar(&gcePemFile, "pem-file", "", "GCE pem file path")
	gceCmd.Flags().StringVar(&gceZone, "zone", "", "GCE Zone where the machines will be started")
	gceCmd.Flags().StringVar(&gceImage, "image", "", "GCE machine image")
	gceCmd.Flags().StringVar(&gceMasterType, "masters-machine-type", "", "GCE machine type for Masters (default: n1-standard-2)")
	gceCmd.Flags().StringVar(&gceNodeType, "nodes-machine-type", "", "GCE machine type for Nodes (default: n1-standard-4)")
	gceCmd.Flags().StringVar(&gceEtcdType, "etcds-machine-type", "", "GCE machine type for Etcds members (default: n1-standard-1)")
	gceCmd.Flags().StringVar(&gceProjectID, "project", "", "GCE project ID")
	gceCmd.Flags().StringVar(&gceSvcAccEmail, "email", "", "GCE service account email")
	gceCmd.Flags().Uint16Var(&etcdCount, "etcds", 0, "Number of etcd, these instances will just act as etcd members")
	gceCmd.Flags().Uint16Var(&masterCount, "masters", 0, "Number of masters, these instances will not run workloads, master components only")
	gceCmd.Flags().Uint16Var(&nodeCount, "nodes", 0, "Number of worker nodes")
	gceCmd.Flags().StringSliceVar(&gceTags, "tags", []string{}, "List of tags")
}
