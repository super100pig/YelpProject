<template>
  <div >
    <h1>商户数据</h1>

    <!-- <div>
      <el-select v-model="filterModule" placeholder="请选择数据">
        <el-option label="数据1" value="数据1"></el-option>
      </el-select>
      <el-button @click="this.show_data" type="primary">显示</el-button>
    </div> -->

<!--    <el-dialog title="系统性能" :visible.sync="dialogTableVisible" @opened="drawBar" width="80%">-->
<!--      <div id="barGraph" style="height: 800px;"></div>-->
<!--    </el-dialog>-->

    <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
    >
      <el-table-column prop="business_id" label="商户ID" width="220" sortable></el-table-column>
      <el-table-column prop="name" label="名称" width="220" sortable></el-table-column>
      <el-table-column prop="address" label="地址" width="220" sortable></el-table-column>
      <el-table-column prop="city" label="城市" sortable></el-table-column>
      <el-table-column prop="stars" label="评星" sortable></el-table-column>
      <el-table-column prop="review_count" label="评论数" sortable></el-table-column>
    </el-table>
  </div>
</template>

<script>
let echarts = require("echarts/lib/echarts");
// 引入柱状图
require("echarts/lib/chart/bar");
// 引入柱状图
require("echarts/lib/chart/pie");
require("echarts/lib/component/tooltip");
require("echarts/lib/component/title");
export default {
  data() {
    return {
      dialogTableVisible: false,
      tableData: [{"business_id":"6iYb2HFDywm3zjuRg0shjw","name":"Oskar Blues Taproom","address":"921 Pearl St","city":"Boulder","stars":4.0,"review_count":86},{"business_id":"tCbdrRPZA0oiIYSmHG3J0w","name":"Flying Elephants at PDX","address":"7000 NE Airport Way","city":"Portland","stars":4.0,"review_count":126},{"business_id":"bvN78flM8NLprQ1a1y5dRg","name":"The Reclaimory","address":"4720 Hawthorne Ave","city":"Portland","stars":4.5,"review_count":13},{"business_id":"oaepsyvc0J17qwi8cfrOWg","name":"Great Clips","address":"2566 Enterprise Rd","city":"Orange City","stars":3.0,"review_count":8},{"business_id":"PE9uqAjdw0E4-8mjGl3wVA","name":"Crossfit Terminus","address":"1046 Memorial Dr SE","city":"Atlanta","stars":4.0,"review_count":14},{"business_id":"D4JtQNTI4X3KcbzacDJsMw","name":"Bob Likes Thai Food","address":"3755 Main St","city":"Vancouver","stars":3.5,"review_count":169},{"business_id":"t35jsh9YnMtttm69UCp7gw","name":"Escott Orthodontics","address":"2511 Edgewater Dr","city":"Orlando","stars":4.5,"review_count":7},{"business_id":"jFYIsSb7r1QeESVUnXPHBw","name":"Boxwood Biscuit","address":"740 S High St","city":"Columbus","stars":4.5,"review_count":11},{"business_id":"N3_Gs3DnX4k9SgpwJxdEfw","name":"Lane Wells Jewelry Repair","address":"7801 N Lamar Blvd, Ste A140","city":"Austin","stars":5.0,"review_count":30},{"business_id":"tXvdYGvlEceDljN8gt2_3Q","name":"Capital City Barber Shop","address":"615 W Slaughter Ln, Ste 113","city":"Austin","stars":4.0,"review_count":5},{"business_id":"rYs_1pNB_RMtn5WQh55QDA","name":"Chautauqua General Store","address":"100 Clematis Dr","city":"Boulder","stars":3.5,"review_count":5},{"business_id":"hCABMnKtwo4Y9alQDxh2kw","name":"Star Kreations Salon and Spa","address":"124 Newbury St, Unit C","city":"Peabody","stars":4.0,"review_count":8},{"business_id":"HPA_qyMEddpAEtFof02ixg","name":"Mr G's Pizza & Subs","address":"474 Lowell St","city":"Peabody","stars":4.0,"review_count":39},{"business_id":"ufCxltuh56FF4-ZFZ6cVhg","name":"Sister Honey's","address":"247 E Michigan St","city":"Orlando","stars":4.5,"review_count":135},{"business_id":"i_t_30RYVUDdZzFIcw80NQ","name":"Uncle Sam's Pawn Shop","address":"225 E Main St","city":"Columbus","stars":4.0,"review_count":5},{"business_id":"g7CEhqBIpwTg6ERcMkCmrQ","name":"Finish Line Car Wash","address":"5510 Memorial Dr","city":"Stone Mountain","stars":2.5,"review_count":11},{"business_id":"GfWJ19Js7wX9rwaHQ7KbGw","name":"Everything POP Shopping & Dining","address":"1050 Century Dr","city":"Orlando","stars":3.0,"review_count":7},{"business_id":"MUeUyqhMja-nnmvgP4rBBg","name":"Saratoga Resort Villas","address":"4787 W Irlo Bronson Hwy","city":"Kissimmee","stars":3.5,"review_count":55},{"business_id":"6fT0lYr_UgWSCZs_w1PBTQ","name":"Salter School","address":"2 Florence St","city":"Malden","stars":2.0,"review_count":5},{"business_id":"dmbbf3AqeG61_QHRZi1M1w","name":"RaceTrac","address":"350 W Sand Lake Rd","city":"Pine Castle","stars":3.5,"review_count":5}],
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
          .get("http://" + localStorage.getItem('backend_host') + "/get_nodes/")
          .then(response => {
            this.tableData = response.data;
          });
    },
    drawBar() {
      this.dialogTableVisible = true;
      // 基于dom，初始化echarts实例
      let barGraph = echarts.init(document.getElementById("barGraph"));
      // 绘制图表
      barGraph.setOption({
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c}"
        },
        legend: {
          left: "center",
          data: ["CPU使用率（%）（真实）", "内存使用率（%）（真实）"
            // , "CPU使用率（%）（预测）", "内存使用率（%）（预测）"
          ]
        },
        xAxis: {
          type: "category",
          name: "日期",
          splitLine: {show: false},
          data: ['2018-01-28', '2018-01-29', '2018-01-30', '2018-01-31', '2018-02-01', '2018-02-02', '2018-02-03', '2018-02-04', '2018-02-05', '2018-02-06', '2018-02-07', '2018-02-08', '2018-02-09', '2018-02-10', '2018-02-11', '2018-02-12', '2018-02-13', '2018-02-14', '2018-02-15', '2018-02-16', '2018-02-17', '2018-02-18', '2018-02-19', '2018-02-20', '2018-02-21', '2018-02-22', '2018-02-23', '2018-02-24', '2018-02-25', '2018-02-26', '2018-02-27', '2018-02-28', '2018-03-01', '2018-03-02', '2018-03-03', '2018-03-04', '2018-03-05', '2018-03-06', '2018-03-07']
        },
        grid: {
          left: "1%",
          right: "8%",
          bottom: "8%",
          containLabel: true
        },
        yAxis: {
          type: "value",
          name: "使用率",
          splitLine: {show: true},
          axisLabel: {
            formatter: function (val) {
              return val * 100 + "%";
            }
          },
          data: [
            "-10%",
            "0%",
            "10%",
            "20%",
            "30%",
            "40%",
            "50%",
            "60%",
            "70%",
            "80%",
            "90%",
            "100%"
          ]
        },
        series: [
          {
            name: "CPU使用率（%）（真实）",
            type: "line",
            data: [0.087, 0.091, 0.209, 0.209, 0.09, 0.086, 0.09, 0.086, 0.091, 0.085, 0.091, 0.09, 0.091, 0.09, 0.091, 0.097, 0.097, 0.09, 0.09, 0.091, 0.097, 0.097, 0.093, 0.089, 0.09, 0.087, 0.091, 0.088, 0.088, 0.089, 0.085, 0.085, 0.089, 0.089, 0.089, 0.087, 0.089, 0.087, 0.086],
            markPoint: {
              symbol: "pin",
              silent: true,
              data: [
                {value: "异常", coord: [2, 0.209]},
                {value: "异常", coord: [3, 0.209]}
              ]
            }
          },
          {
            name: "内存使用率（%）（真实）",
            type: "line",
            data: [0.003946652902577071, 0.003984916033737075, 0.0069282095850319025, 0.0069282095850319025, 0.003987498256999298, 0.003950580788911607, 0.003970659251782261, 0.003983895084119323, 0.003970077342314718, 0.003987822970453857, 0.003984625079003303, 0.003987822970453857, 0.003987498256999298, 0.0040399038337043496, 0.003986589023456262, 0.003983895084119323, 0.003983895084119323, 0.003982297441133129, 0.003983895084119323, 0.003965167481182321, 0.0040585249244754745, 0.0040585249244754745, 0.004049180660558896, 0.0040585249244754745, 0.004058527581381311, 0.0040585249244754745, 0.004059836877683284, 0.003983895084119323, 0.003983895084119323, 0.004015248064732773, 0.003987822970453857, 0.003987822970453857, 0.0045544235557534365, 0.003987822970453857, 0.003987822970453857, 0.003988080166466842, 0.003983895084119323, 0.0039868436088483115, 0.003983895084119323],
            markPoint: {
              symbol: "pin",
              silent: true,
              data: [
                {value: "异常", xAxis: 2, yAxis: 0.0069282095850319025},
                {value: "异常", xAxis: 3, yAxis: 0.0069282095850319025}
              ]
            }
          }
          // ,{
          //   name: "CPU使用率（%）（预测）",
          //   type: "line",
          //   data: [0.14781057834625244, 0.1478106677532196, 0.1479136049747467, 0.12073993682861328, 0.12065604329109192, 0.12065732479095459, 0.09661652147769928, 0.09661619365215302, 0.09661619365215302, 0.07401201128959656, 0.07401201128959656, 0.07401126623153687, 0.054805487394332886, 0.05482158064842224, 0.054804980754852295, 0.04073801636695862, 0.04073801636695862, 0.04073795676231384, 0.03312121331691742, 0.03312121331691742, 0.033125683665275574, 0.031947970390319824, 0.031947970390319824, 0.03194248676300049, 0.03679579496383667, 0.03679615259170532, 0.03679618239402771, 0.04633133113384247, 0.04633133113384247, 0.04633133113384247, 0.059132128953933716, 0.059132128953933716, 0.059153616428375244, 0.07347133755683899, 0.07347133755683899, 0.07347133755683899, 0.08799730241298676, 0.08799730241298676, 0.08799697458744049]
          // },
          // {
          //   name: "内存使用率（%）（预测）",
          //   type: "line",
          //   data: [0.018665969371795654, 0.01866590976715088, 0.01859152317047119, 0.04463773965835571, 0.044696927070617676, 0.04469597339630127, 0.06451761722564697, 0.06451791524887085, 0.06451785564422607, 0.07658600807189941, 0.07658594846725464, 0.07658651471138, 0.08037349581718445, 0.08036236464977264, 0.08037382364273071, 0.07624444365501404, 0.07624444365501404, 0.07624447345733643, 0.06531330943107605, 0.06531327962875366, 0.0653100311756134, 0.049256831407547, 0.049256861209869385, 0.04926091432571411, 0.03011864423751831, 0.030118346214294434, 0.030118346214294434, 0.010067373514175415, 0.010067373514175415, 0.010067373514175415, -0.008785426616668701, -0.008785426616668701, -0.008801043033599854, -0.02456498146057129, -0.02456498146057129, -0.02456498146057129, -0.03588593006134033, -0.03588593006134033, -0.03588569164276123]
          // }
        ]
      });
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    }
  }
};
</script>