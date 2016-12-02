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

package cloud

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

type AnsibleGCETask struct {
	MachineType         string `json:"machine_type"`
	ProjectID           string `json:"project_id"`
	ServiceAccountEmail string `json:"service_account_email"`
	Image               string `json:"image"`
	InstanceNames       string `json:"instance_names"`
	Zone                string `json:"zone"`
	PemFile             string `json:"pem_file"`
}

type AnsibleCopyTask struct {
	Dest    string `json:"dest"`
	Content string `json:"content"`
}

type AnsibleWaitForTask struct {
	Port    int    `json:"port"`
	State   string `json:"state"`
	Host    string `json:"host"`
	Timeout int    `json:"timeout"`
	Module  string `json:"module"`
}

type AnsibleGCEPlaybook struct {
	Become bool `json:"become"`
	Tasks  []struct {
		AnsibleGCETask     `json:"gce,omitempty"`
		Name               string `json:"name"`
		Register           string `json:"register,omitempty"`
		AnsibleCopyTask    `json:"copy,omitempty"`
		WithItems          string `json:"with_items,omitempty"`
		AnsibleWaitForTask `json:"local_action,omitempty"`
	} `json:"tasks"`
	Hosts       string `json:"hosts"`
	GatherFacts bool   `json:"gather_facts"`
}

// type AnsibleGCEPlaybook struct {
// 	Become bool `json:"become"`
// 	Tasks  []struct {
// 		Gce struct {
// 			MachineType         string `json:"machine_type"`
// 			ProjectID           string `json:"project_id"`
// 			ServiceAccountEmail string `json:"service_account_email"`
// 			Image               string `json:"image"`
// 			InstanceNames       string `json:"instance_names"`
// 			Zone                string `json:"zone"`
// 			PemFile             string `json:"pem_file"`
// 		} `json:"gce,omitempty"`
// 		Name     string `json:"name"`
// 		Register string `json:"register,omitempty"`
// 		Copy     struct {
// 			Dest    string `json:"dest"`
// 			Content string `json:"content"`
// 		} `json:"copy,omitempty"`
// 		WithItems   string `json:"with_items,omitempty"`
// 		LocalAction struct {
// 			Port    int    `json:"port"`
// 			State   string `json:"state"`
// 			Host    string `json:"host"`
// 			Timeout int    `json:"timeout"`
// 			Module  string `json:"module"`
// 		} `json:"local_action,omitempty"`
// 	} `json:"tasks"`
// 	Hosts       string `json:"hosts"`
// 	GatherFacts bool   `json:"gather_facts"`
// }

func genGCEPlaybook(ansiblePlaybook *AnsibleGCEPlaybook) string {
	fmt.Print(ansiblePlaybook)
	return ("path")
}

//CreateGCEInstances runs the ansible-playbook command that creates the vms
func CreateGCEInstances(ansiblePlaybook *AnsibleGCEPlaybook) {
	pBookFile := genGCEPlaybook(ansiblePlaybook)
	fmt.Println(pBookFile)
	output, _ := json.Marshal(ansiblePlaybook)
	ioutil.WriteFile("output.json", output, 0644)
}
