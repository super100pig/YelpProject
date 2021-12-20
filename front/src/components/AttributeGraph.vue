<template>
  <div style="margin-left:20px;margin-top:20px;">
    <el-row type="flex" :gutter="20">
      <el-col :span="7">
        <a style="font-size: small">零件编号：</a>
        <el-input style="width: 300px" v-model="selectedNode" placeholder="请输入零件编号"></el-input>
      </el-col>
    </el-row>
    <el-row type="flex" :gutter="20">
      <el-col :span="7">
        <a style="font-size: small">邻居阶数：</a>
        <el-select style="width: 300px" v-model="neighDegree" placeholder="请选择邻居阶数">
          <el-option label="1" value="1"></el-option>
          <el-option label="2" value="2"></el-option>
          <el-option label="3" value="3"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        <el-button type="primary">可视化结果</el-button>
      </el-col>
    </el-row>
    <el-dialog title="训练参数" :visible.sync="setParametersVisible">
      <el-form :model="parameters">
        <el-form-item label="最小支持度" :label-width="formLabelWidth">
          <el-input v-model="parameters.support" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="最小置信度" :label-width="formLabelWidth">
          <el-input v-model="parameters.conf" autocomplete="off"></el-input>
        </el-form-item>
        <!-- <el-form-item label="最小关联元数" :label-width="formLabelWidth">
          <el-input v-model="parameters.min_item_num" autocomplete="off"></el-input>
        </el-form-item> -->
        <el-form-item label="滑窗步长" :label-width="formLabelWidth">
          <el-input v-model="parameters.step" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="窗口大小" :label-width="formLabelWidth">
          <el-input v-model="parameters.window" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="setParametersVisible = false">取 消</el-button>
        <el-button type="primary" @click="setParametersVisible = false">确 定</el-button>
      </div>
    </el-dialog>
    <div id="neo4jd3" style="height: 800px;"></div>
  </div>
</template>

<script>
// document.getElementById('neo4jd3').style.display = '';
function rel2DataRelationship(r) {
  return r;
}
function graphNode2DataNode(r) {
  return r;
}
var neo4jd3Instance;

let screen_height, screen_width;

function init() {
  const eleId = "neo4jd3";
  console.log(document.getElementById(eleId));
  document.getElementById(eleId).innerHTML = "";
  // @ts-ignore
  // eslint-disable-next-line no-undef
  let temp_neo4jd3Instance = new Neo4jd3("#neo4jd3", {
    highlight: [],
    red_rel: [],
    icons: {
      客户: "user",
      person: "user",
      Person: "user",
      Relation: "yelp",
      基金: "money",
      项目: "database",
      Company: "university",
      People: "handshake-o",
      stock: "credit-card",
      User: "user",
      Business: "yelp",
      Industry: "database",
      Shareholder: "money",
      Module: "database",
      Component: 'gear,cog'
    },
    images: {
      Contributor: "https://eisman.github.io/neo4jd3/img/twemoji/1f38f.svg",
      Project: "https://eisman.github.io/neo4jd3/img/twemoji/1f5c3.svg"
    },
    minCollision: 60,
    neo4jData: { results: [], errors: [] },
    nodeRadius: 30,
    onNodeDoubleClick: onNodeDoubleClicked,
    onRelationshipDoubleClick: onRelationshipDoubleClicked,
    zoomFit: false
  });
  screen_height = temp_neo4jd3Instance.get_screen_height();
  screen_width = temp_neo4jd3Instance.get_screen_width();
  console.log(screen_width, screen_height);
  return temp_neo4jd3Instance;
}

// eslint-disable-next-line no-unused-vars
function onNodeDoubleClicked(node) {
  // console.log("double click on node: ", node);
}

function onRelationshipDoubleClicked(relationship) {
  console.log("double click on relationship: ", relationship);
}

function show_data(graph_data) {
  let temp;
  neo4jd3Instance = init();
  // (document.getElementById("select_id3") as HTMLSelectElement).disabled = false;
  temp = graph_data;
  // console.log("出现了！res");
  // console.log(res);
  const d3Data = {
    nodes: [],
    relationships: []
  };
  for (let i in temp.nodes) {
    d3Data.nodes.push(graphNode2DataNode(temp.nodes[i]));
  }

  let important_rel = [];
  for (let i in temp.relationships) {
    d3Data.relationships.push(rel2DataRelationship(temp.relationships[i]));

    if (temp.relationships[i].type === "Recommend") {
      important_rel.push(temp.relationships[i].id);
    }
  }
  // console.log("important_rel", important_rel);
  // console.info(d3Data);
  neo4jd3Instance.replaceWithD3Data(d3Data, [], important_rel);
}
let module_id_map = {
  AS: 1,
  CCS: 2,
  AAA: 3,
  MDU: 4,
  VOD: 5,
  GBSG: 6,
  SA: 7
};
let rel_id = 100;
let graph_data = {
  "nodes": [
    {
      "labels": [
        "Component"
      ],
      "id": 1,
      "properties": {
        "name": "Component 1",
        "status": "black"
      },
      "showName": "Component 1"
    },
    {
      "labels": [
        "Component"
      ],
      "id": 2,
      "properties": {
        "name": "Component 2",
        "status": "gray"
      },
      "showName": "Component 2"
    },
    {
      "labels": [
        "Component"
      ],
      "id": 3,
      "properties": {
        "name": "Component 3",
        "status": "gray"
      },
      "showName": "Component 3"
    },
    {
      "labels": [
        "Component"
      ],
      "id": 4,
      "properties": {
        "name": "Component 4",
        "status": "black"
      },
      "showName": "Component 4"
    },
    {
      "labels": [
        "Component"
      ],
      "id": 5,
      "properties": {
        "name": "Component 5",
        "status": "white"
      },
      "showName": "Component 5"
    },
    {
      "labels": [
        "Component"
      ],
      "id": 6,
      "properties": {
        "name": "Component 6",
        "status": "white"
      },
      "showName": "Component 6"
    },
    {
      "labels": [
        "Component"
      ],
      "id": 7,
      "properties": {
        "name": "Component 7",
        "status": "white"
      },
      "showName": "Component 7"
    }
  ],
  "relationships": [
    {
      "startNode": 2,
      "endNode": 3,
      "source": 2,
      "target": 3,
      "id": 201,
      "type": "rel2",
      "properties": {},
      "linknum": "1",
      "showName": ""
    },
    {
      "startNode": 1,
      "endNode": 4,
      "source": 1,
      "target": 4,
      "id": 202,
      "type": "rel2",
      "properties": {},
      "linknum": "1",
      "showName": ""
    },
    {
      "startNode": 4,
      "endNode": 3,
      "source": 4,
      "target": 3,
      "id": 203,
      "type": "rel2",
      "properties": {},
      "linknum": "1",
      "showName": ""
    },
    {
      "startNode": 4,
      "endNode": 6,
      "source": 4,
      "target": 6,
      "id": 204,
      "type": "rel2",
      "properties": {},
      "linknum": "1",
      "showName": ""
    },
    {
      "startNode": 5,
      "endNode": 6,
      "source": 5,
      "target": 6,
      "id": 205,
      "type": "rel2",
      "properties": {},
      "linknum": "1",
      "showName": ""
    },
    {
      "startNode": 6,
      "endNode": 7,
      "source": 6,
      "target": 7,
      "id": 206,
      "type": "rel2",
      "properties": {},
      "linknum": "1",
      "showName": ""
    }
  ]
};
let select_mode = false;
let exist_relations = [];
export default {
  data() {
    return {
      selectedNode: "Component 4",
      neighDegree: "2",
      time_range: [new Date(2018, 0, 1, 0, 0), new Date(2020, 11, 31, 23, 59)],
      select_mode_val: false,
      setParametersVisible: false,
      parameters: {
        support: 0.01,
        conf: 0.1,
        min_item_num: 2,
        step: 1,
        window: 2
      },
      formLabelWidth: "110px"
    };
  },
  mounted() {
    let flag = localStorage.getItem("flag");
    if (flag === 'false') {
      let ex_graph_data = JSON.parse(JSON.stringify(graph_data));
      for (let i = 0; i < graph_data['nodes'].length; i++) {
        if (ex_graph_data['nodes'][i]['properties']['status'] === 'gray') {
          ex_graph_data['nodes'][i]['properties']['status'] = 'white';
        }
      }
      show_data(ex_graph_data);
    } else {
      show_data(graph_data);
    }
  },
  methods: {
    switch_change_select_mode() {
      console.log("change");
      select_mode = !select_mode;
      neo4jd3Instance.change_select_mode(select_mode);
    },
    btn_clear_relationship() {
      show_data(graph_data);
      exist_relations = [];
      this.select_mode_val = false;
      select_mode = false;
      neo4jd3Instance.change_select_mode(false);
    },
    btn_search_relationship() {
      let module2search = neo4jd3Instance.get_select_info();
      if (module2search.length === 0) {
        return;
      }
      console.log(module2search);
      console.log(this.time_range[0].getTime(), this.time_range[1].getTime());
      let new_relationships = [];
      let edge_count = 0;
      for (let i = 0; i < module2search.length; i++) {
        for (let j = i + 1; j < module2search.length; j++) {
          if (Math.random()>0.5) {
            continue;
          }
          let id_i = module_id_map[module2search[i]];
          let id_j = module_id_map[module2search[j]];
          if (exist_relations.indexOf(id_i + "#" + id_j) > -1) {
            console.log(id_i + "#" + id_j, "跳过");
            continue;
          }
          edge_count += 1;
          exist_relations.push(id_i + "#" + id_j);
          console.log(exist_relations);
          new_relationships.push({
            startNode: id_i,
            endNode: id_j,
            source: id_i,
            target: id_j,
            id: rel_id,
            type: "rel",
            properties: {},
            linknum: "1",
            showName: Math.round(Math.random() * 1000) / 1000
          });
          rel_id++;
        }
      }
      if (edge_count === 0) {
        this.$message('无边新增！');
      }
      neo4jd3Instance.updateWithD3Data({
        nodes: [],
        relationships: new_relationships
      });
      this.select_mode_val = false;
      select_mode = false;
      console.log("change");
      neo4jd3Instance.change_select_mode(false);
    },
    btn_set_parameters() {
      this.setParametersVisible = true;
    }
  }
};
</script>
