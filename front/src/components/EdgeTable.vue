<template>
  <div style="margin-left:20px;margin-top:20px;">
    <div>
      <el-select v-model="filterModule" placeholder="请选择数据">
        <el-option label="数据1" value="数据1"></el-option>
        <el-option label="数据2" value="数据2"></el-option>
      </el-select>
      <el-button @click="this.show_data" type="primary">显示</el-button>
    </div>

    <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
    >
      <el-table-column prop="left_node" label="头零件名称" width="120" sortable></el-table-column>
      <el-table-column prop="right_node" label="尾零件名称" width="120" sortable></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogTableVisible: false,
      tableData: [
        {'left_node': 2155330, 'right_node': 2155331},
        {'left_node': 2155331, 'right_node': 2155330},
        {'left_node': 322051, 'right_node': 2353780},
        {'left_node': 322051, 'right_node': 2353781},
        {'left_node': 322051, 'right_node': 1875971},
        {'left_node': 360886, 'right_node': 1875972},
        {'left_node': 360886, 'right_node': 1929991},
        {'left_node': 360886, 'right_node': 2058325},
        {'left_node': 873943, 'right_node': 1062249},
        {'left_node': 1062249, 'right_node': 873943}
        /*
        2155330	2155331
        2155331	2155330
        322051	2353780
        322051	2353781
        360886	1875971
        360886	1875972
        360886	1929991
        360886	2058325
        873943	1062249
        1062249	873943
        */
      ],
      time_range: [new Date(2018, 0, 28), new Date(2020, 2, 1)],
      filterModule: "数据1"
    };
  },
  mounted() {
    this.show_data();
  },
  methods: {
    show_data() {
      this.$axios
          .get("http://" + localStorage.getItem('backend_host') + "/get_edges/")
          .then(response => {
            this.tableData = response.data;
          });
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    }
  }
};
</script>