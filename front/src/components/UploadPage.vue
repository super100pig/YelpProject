<template>
  <div>
    <el-row>
      <el-col>
        <a>点数据所在目录：</a>
        <el-input value="D:/node1.csv"></el-input>
      </el-col>
      <el-col>
        <a>边数据所在目录：</a>
        <el-input value="D:/edge1.csv"></el-input>
      </el-col>
      <el-col>
        <a>数据名称：</a>
        <el-input value="数据1"></el-input>
      </el-col>
    </el-row>
    <el-button type="primary" @click="open1">
      上传
    </el-button>
  </div>
</template>

<script>
function wait(ms) {
  return new Promise(resolve => setTimeout(() =>resolve(), ms));
}
export default {
  data() {
    return {algorithm: ""}
  },
  methods: {
    open1() {
      this.$message('数据正在上传……');
      wait(3000).then(()=>{
        this.$message({
          message: '上传成功！',
          type: 'success'
        });
      })
    }
  }
}
</script>