<template>
  <div style="margin-left:20px;margin-top:20px;">
    <div>
      <el-select v-model="filterModule" placeholder="请选择数据">
        <el-option label="数据1" value="数据1"></el-option>
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
      <el-table-column prop="device_id" label="设备id" width="120" sortable></el-table-column>
      <el-table-column prop="score" label="分数" width="240" sortable></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogTableVisible: false,
      tableData: [
        {'device_id': 1330165, 'score': 0},
        {'device_id': 1204989, 'score': 0},
        {'device_id': 1514576, 'score': 0},
        {'device_id': 1893100, 'score': 0},
        {'device_id': 107796, 'score': 1},
        {'device_id': 1019072, 'score': 0},
        {'device_id': 2122335, 'score': 0},
        {'device_id': 1399821, 'score': 0},
        {'device_id': 1799873, 'score': 0},
        {'device_id': 1875400, 'score': 0}
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
          .get("http://" + localStorage.getItem('backend_host') + "/get_devices/")
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