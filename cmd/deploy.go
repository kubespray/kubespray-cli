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
	"log"
	"os/user"

	"github.com/spf13/cobra"
)

var (
	PromptPasswd bool
	AWS          bool
	GCE          bool
	CoreOS       bool
	Passwd       string
	User         string
	KubeVersion  string
	NetPlugin    string
	AnsibleUser  string
	SSHKey       string
)

// deployCmd represents the deploy command
var deployCmd = &cobra.Command{
	Use:   "deploy",
	Short: "Deploy the Kubernetes cluster using Ansible",
	Long:  "",

	Run: runDeploy,
}

func init() {
	RootCmd.AddCommand(deployCmd)
	deployCmd.Flags().BoolVarP(&PromptPasswd, "prompt-passwd", "P", false, "Set 'kube' user passwd to authenticate to the API (Interactive mode)")
	deployCmd.Flags().BoolVar(&AWS, "aws", false, "Instances are running on AWS")
	deployCmd.Flags().BoolVar(&GCE, "gce", false, "Instances are running on GCE")
	deployCmd.Flags().BoolVar(&CoreOS, "coreos", false, "bootstrap python on CoreOS")
	deployCmd.Flags().StringVar(&Passwd, "passwd", "", "Set 'kube' user passwd to authenticate to the API (default: 'changeme')")
	deployCmd.Flags().StringVarP(&KubeVersion, "kube-version", "V", "", "Choose the kubernetes version to be installed")
	deployCmd.Flags().StringVarP(&NetPlugin, "network-plugin", "n", "", "Choose the kubernetes version to be installed (default: 'flannel')")
	deployCmd.Flags().StringVarP(&AnsibleUser, "user", "u", "", "Ansible SSH user (remote user, default is the current username")
	deployCmd.Flags().StringVarP(&SSHKey, "sshkey", "k", "", "SSH key to use to authenticate to remote hosts (default: ''~/.ssh/id.rsa')")
}

func runDeploy(cmd *cobra.Command, args []string) {

	if User == "" {
		usr, err := user.Current()
		if err != nil {
			log.Fatal(err)
		}
		username := usr.Username
		fmt.Println(username)
	}
}
