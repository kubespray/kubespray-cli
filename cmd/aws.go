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
	usePrivIP      bool
	assignPublicIP bool
	awsAccessKey   string
	awsSecretKey   string
	awsAmi         string
	awsMasterType  string
	awsNodeType    string
	awsEtcdType    string
	awsRegion      string
	awsVpcID       string
	awsSubnetID    string
	awsSGID        string
	awsSGName      string
	etcdCount      uint16
	masterCount    uint16
	nodeCount      uint16
	awsTags        []string
)

// awsCmd represents the aws command
var awsCmd = &cobra.Command{
	Use:   "aws",
	Short: "Run instances on Amazon Web Services",
	Long:  "",
	Run:   runHelp,
}

func init() {
	RootCmd.AddCommand(awsCmd)
	awsCmd.Flags().BoolVar(&usePrivIP, "use-private-ip", false, "If set to true, using the private ip for SSH connection")
	awsCmd.Flags().BoolVar(&assignPublicIP, "assign-public-ip", false, "when provisioning within vpc, assign a public IP address")
	awsCmd.Flags().StringVar(&awsAccessKey, "aws-access-key", "", "AWS access key")
	awsCmd.Flags().StringVar(&awsSecretKey, "aws-secret-key", "", "AWS secret key")
	awsCmd.Flags().StringVar(&awsAmi, "ami", "", "Amazon Machine Image ")
	awsCmd.Flags().StringVar(&awsRegion, "region", "", "AWS region")
	awsCmd.Flags().StringVar(&awsMasterType, "masters-instance-type", "", "AWS instance type for Masters (default: t2.medium)")
	awsCmd.Flags().StringVar(&awsNodeType, "nodes-instance-type", "", "AWS instance type for Nodes (default: t2.large)")
	awsCmd.Flags().StringVar(&awsEtcdType, "etcds-instance-type", "", "AWS instance type for Etcds members (default: t2.small)")
	awsCmd.Flags().StringVar(&awsVpcID, "vpc-id", "", "AWS VPC ID")
	awsCmd.Flags().StringVar(&awsSubnetID, "subnet-id", "", "AWS subnet id")
	awsCmd.Flags().StringVar(&awsSGName, "security-group-name", "", "AWS security group name")
	awsCmd.Flags().StringVar(&awsSGID, "security-group-id", "", "AwS security group id")
	awsCmd.Flags().Uint16Var(&etcdCount, "etcds", 0, "Number of etcd, these instances will just act as etcd members")
	awsCmd.Flags().Uint16Var(&masterCount, "masters", 0, "Number of masters, these instances will not run workloads, master components only")
	awsCmd.Flags().Uint16Var(&nodeCount, "nodes", 0, "Number of worker nodes")
	awsCmd.Flags().StringSliceVar(&awsTags, "tags", []string{}, "List of tags in the form of 'name=value'")
}
