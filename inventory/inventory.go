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

package inventory

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path"
	"strings"

	uuid "github.com/satori/go.uuid"
	ini "gopkg.in/ini.v1"
)

var (
	kargoPath string
	host      string
)

func checkErr(err error) {
	if err != nil {
		log.Fatal("ERROR:", err)
	}
}

type ansibleHost struct {
	Name     string            `json:"name"`
	Hostvars map[string]string `json:"hostvars"`
}

type ansibleGroup struct {
	Name  string                  `json:"name"`
	Hosts map[string]*ansibleHost `json:"hosts"`
}

func WritelocalInventory(kargoPath string) {
	data := "local ansible_ssh_host=localhost ansible_python_interpreter=python2 ansible_connection=local"
	localcfg := path.Join(kargoPath, "local.cfg")
	f, err := os.Create(localcfg)
	checkErr(err)
	f.WriteString(data)
}

func ReadInventory(path string) {
	fmt.Println("do something")
}

func CreateInventory(ClusterName string, e uint16, m uint16, n uint16) uint16 {
	// etcds := &ansibleGroup{
	// 	Name:  "etcd",
	// 	Hosts: make(map[string]*ansibleHost),
	// }
	masters := &ansibleGroup{
		Name:  "master",
		Hosts: make(map[string]*ansibleHost),
	}
	// nodes := &ansibleGroup{
	// 	Name:  "node",
	// 	Hosts: make(map[string]*ansibleHost),
	// }
	for i := 1; i <= int(n); i++ {
		hostID := uuid.NewV4().String()[:8]
		s := []string{ClusterName, hostID}
		hostName := strings.Join(s, "-")

		host := &ansibleHost{
			Name: hostName,
			Hostvars: map[string]string{
				"var1": "value1",
			},
		}
		masters.Hosts[hostName] = host
	}
	b, _ := json.Marshal(masters)
	fmt.Println(string(b))
	return n
}

func WriteInventory(etcd *ansibleGroup, nodes *ansibleGroup, masters *ansibleGroup) {
	fmt.Println("do something")
}

func main() {
	blah := make(map[string]string)
	blah["toto"] = "titi"
	fmt.Printf("%s", blah["toto"])
	pp := &ansibleHost{
		Name: "tu",
		Hostvars: map[string]string{
			"john": "doe",
			"will": "smith",
		},
	}
	pp.Hostvars["salam"] = "alaykoum"
	fmt.Println(pp)
	masters := &ansibleGroup{
		Name:  "masters",
		Hosts: make(map[string]*ansibleHost),
	}
	masters.Hosts["pp"] = pp
	fmt.Println(masters.Hosts["pp"])
	b, _ := json.Marshal(masters)
	print(string(b))
	cfg := ini.Empty()
	cfg.NewSection("all")
	cfg.SaveTo("test.cfg")
}
