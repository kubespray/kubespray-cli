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
	manAddNode     uint16
	manAddEtcd     uint16
	manAddMaster   uint16
	destroyCluster string
)

// manageCmd represents the manage command
var manageCmd = &cobra.Command{
	Use:   "manage",
	Short: "Manage a running cluster",
	Long:  "",
	Run:   runHelp,
}

func init() {
	RootCmd.AddCommand(manageCmd)
	manageCmd.Flags().Uint16Var(&manAddNode, "add-node", 0, "Number of nodes to add to a running cluster")
	manageCmd.Flags().Uint16Var(&manAddEtcd, "add-etcd", 0, "Number of etcd members to add to a running cluster")
	manageCmd.Flags().Uint16Var(&manAddMaster, "add-master", 0, "Number of masters to add to a running cluster")
	manageCmd.Flags().StringVar(&destroyCluster, "destroy", "", "Name of the running cluster to destroy, instances will be terminated")
}
