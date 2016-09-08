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
	floatingIP     bool
	OSAuthURL      string
	OSUsername     string
	OSPassword     string
	OSProjectName  string
	OSNetwork      string
	OSEtcdFlavor   string
	OSNodeFlavor   string
	OSMasterFlavor string
)

// openstackCmd represents the openstack command
var openstackCmd = &cobra.Command{
	Use:   "openstack",
	Short: "Run instances on Openstack",
	Long:  "",
	Run:   runOpenStack,
}

func init() {
	RootCmd.AddCommand(openstackCmd)
	gceCmd.Flags().BoolVar(&floatingIP, "floating-ip", false, "If set to true, assign public IP")
	gceCmd.Flags().StringVar(&OSAuthURL, "os-auth-url", "", "OpenStack authentication URL")
	gceCmd.Flags().StringVar(&OSUsername, "os-username", "", "OpenStack username")
	gceCmd.Flags().StringVar(&OSPassword, "os-password", "", "OpenStack password")
	gceCmd.Flags().StringVar(&OSProjectName, "os-project-name", "", "OpenStack project name")
	gceCmd.Flags().StringVar(&OSNetwork, "neutron-network", "", "Neutron network name")
	gceCmd.Flags().StringVar(&OSEtcdFlavor, "etcds-flavor", "", "OpenStack instance flavor for Etcd")
	gceCmd.Flags().StringVar(&OSNodeFlavor, "nodes-flavor", "", "OpenStack instance flavor for Nodes")
	gceCmd.Flags().StringVar(&OSMasterFlavor, "masters-flavor", "", "OpenStack instance flavor for Masters")
	gceCmd.Flags().Uint16Var(&etcdCount, "etcds", 0, "Number of etcd, these instances will just act as etcd members")
	gceCmd.Flags().Uint16Var(&masterCount, "masters", 0, "Number of masters, these instances will not run workloads, master components only")
	gceCmd.Flags().Uint16Var(&nodeCount, "nodes", 0, "Number of worker nodes")
}

func runOpenStack(cmd *cobra.Command, args []string) {
	if nodeCount == 0 {
		cmd.Help()
		Log.Fatal("Option 'nodes' is required. Number of nodes to run")
	}
}
