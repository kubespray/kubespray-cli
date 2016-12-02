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
	"github.com/smana/kargo/inventory"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	usePrivIP      bool
	assignPublicIP bool
	AwsAccessKey   string
	AwsSecretKey   string
	AwsAmi         string
	AwsMasterType  string
	AwsNodeType    string
	AwsEtcdType    string
	AwsRegion      string
	AwsVpcID       string
	AwsSubnetID    string
	AwsSGID        string
	AwsSGName      string
	AwsTags        []string
)

// awsCmd represents the aws command
var awsCmd = &cobra.Command{
	Use:   "aws",
	Short: "Run instances on Amazon Web Services",
	Long:  "",
	Run:   runAWS,
}

func init() {
	RootCmd.AddCommand(awsCmd)
	awsCmd.Flags().BoolVar(&usePrivIP, "use-private-ip", false, "If set to true, using the private ip for SSH connection")
	awsCmd.Flags().BoolVar(&assignPublicIP, "assign-public-ip", false, "when provisioning within vpc, assign a public IP address")
	awsCmd.Flags().BoolVar(&noClone, "noclone", false, "Do not clone the git repo. Useful when the repo is already downloaded")
	awsCmd.Flags().StringVar(&AwsAccessKey, "aws-access-key", "", "AWS access key")
	awsCmd.Flags().StringVar(&AwsSecretKey, "aws-secret-key", "", "AWS secret key")
	awsCmd.Flags().StringVar(&AwsAmi, "ami", "", "Amazon Machine Image ")
	awsCmd.Flags().StringVar(&AwsRegion, "region", "", "AWS region")
	awsCmd.Flags().StringVar(&AwsMasterType, "masters-instance-type", "", "AWS instance type for Masters (default: t2.medium)")
	awsCmd.Flags().StringVar(&AwsNodeType, "nodes-instance-type", "", "AWS instance type for Nodes (default: t2.large)")
	awsCmd.Flags().StringVar(&AwsEtcdType, "etcds-instance-type", "", "AWS instance type for Etcds members (default: t2.small)")
	awsCmd.Flags().StringVar(&AwsVpcID, "vpc-id", "", "AWS VPC ID")
	awsCmd.Flags().StringVar(&AwsSubnetID, "subnet-id", "", "AWS subnet id")
	awsCmd.Flags().StringVar(&AwsSGName, "security-group-name", "", "AWS security group name")
	awsCmd.Flags().StringVar(&AwsSGID, "security-group-id", "", "AwS security group id")
	awsCmd.Flags().StringVar(&ClusterName, "cluster-name", "", "Cluster name, ramdom word if not set")
	awsCmd.Flags().Uint16Var(&etcdCount, "etcds", 0, "Number of etcd, these instances will just act as etcd members")
	awsCmd.Flags().Uint16Var(&masterCount, "masters", 0, "Number of masters, these instances will not run workloads, master components only")
	awsCmd.Flags().Uint16Var(&nodeCount, "nodes", 0, "Number of worker nodes")
	awsCmd.Flags().StringSliceVar(&AwsTags, "tags", []string{}, "List of tags in the form of 'name=value'")
}

func runAWS(cmd *cobra.Command, args []string) {
	// Clone Kargo repository
	if !noClone {
		if common.PathExists(viper.GetString("KargoPath")) {
			if nodeCount == 0 {
				cmd.Help()
				Log.Fatal("Option 'nodes' is required. Number of nodes to run")
			}
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
	if ClusterName == "" {
		ClusterName := common.SetClusterName()
		inventory.CreateInventory(ClusterName, etcdCount, masterCount, nodeCount)
	} else {
		inventory.CreateInventory(ClusterName, etcdCount, masterCount, nodeCount)
	}
	inventory.WritelocalInventory(viper.GetString("KargoPath"))

}
