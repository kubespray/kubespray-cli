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

	"github.com/fatih/color"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	redPrint      = color.New(color.FgHiRed).SprintFunc()
	yellowPrint   = color.New(color.FgHiYellow).SprintFunc()
	greenPrint    = color.New(color.FgHiGreen).SprintFunc()
	cfgFile       string
	kargoPath     string
	inventoryPath string
	etcdCount     uint16
	masterCount   uint16
	nodeCount     uint16
)

// RootCmd represents the base command when called without any subcommands
var RootCmd = &cobra.Command{
	Use:   "kargo",
	Short: "Deploy a production ready Kubernetes cluster",
	Long: `Kargo is a command line wrapper which deploys a production ready
Kubernetes cluster using kargo (http://kargo.kubespray.io)`,
	Run: runHelp,
}

// Execute adds all child commands to the root command sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	if err := RootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(-1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)
	RootCmd.PersistentFlags().StringVarP(&cfgFile, "config", "c", "", "config file (default is $HOME/.kargo.yaml)")
	RootCmd.PersistentFlags().StringVarP(&kargoPath, "path", "p", "", "Where kargo will be installed")
	RootCmd.PersistentFlags().StringVarP(&inventoryPath, "inventory", "i", "", "Inventory file path. Defaults to <path parameter>/inventory/inventory.cfg")
	RootCmd.PersistentFlags().BoolP("assumeyes", "y", false, "When a yes/no prompt would be presented, assume that the user entered 'yes'")
}

//Set default configuration values
func loadDefaultSettings() {
	//AWS
	viper.SetDefault("awsMasterType", "t2.medium")
	viper.SetDefault("awsNodeType", "t2.large")
	viper.SetDefault("awsEtcdType", "t2.small")
	viper.SetDefault("awsVpcID", "default")
	viper.SetDefault("awsSubnetID", "default")
	viper.SetDefault("awsSGName", "default")
	//GCE
	viper.SetDefault("gceMasterType", "n1-standard-2")
	viper.SetDefault("gceNodeType", "n1-standard-4")
	viper.SetDefault("gceEtcdType", "n1-standard-1")
}

//Bind flags values to viper config
func bindFlags() {
	viper.BindPFlag("aws-access-key", awsCmd.Flags().Lookup("aws-access-key"))
	viper.BindPFlag("aws-secret-key", awsCmd.Flags().Lookup("aws-secret-key"))
	viper.BindPFlag("masters-instance-type", awsCmd.Flags().Lookup("masters-instance-type"))
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
	if cfgFile != "" { // enable ability to specify config file via flag
		viper.SetConfigFile(cfgFile)
	} else {
		viper.SetConfigName(".kargo") // name of config file (without extension)
		viper.AddConfigPath("$HOME")  // adding home directory as first search path
		viper.AutomaticEnv()          // read in environment variables that match
	}

	err := viper.ReadInConfig() // Find and read the config file
	if err != nil {             // Handle errors reading the config file
		panic(fmt.Errorf("%s Fatal error config file: %s \n", redPrint("ERROR:"), err))
	}

	loadDefaultSettings()

	bindFlags()
}

func runHelp(cmd *cobra.Command, args []string) {
	cmd.Help()
}
