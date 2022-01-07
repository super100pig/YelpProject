<template> 

  <div>
    <h1>请输入文件路径</h1>
    <div style="margin-top: 15px;">
      <el-input placeholder="*.json" v-model="input1">
        <template slot="prepend">商户数据所在目录</template>
      </el-input>
    </div>
    <div style="margin-top: 15px;">
      <el-input placeholder="*.json" v-model="input2">
        <template slot="prepend">用户数据所在目录</template>
      </el-input>
    </div>
    <div style="margin-top: 15px;">
      <el-input placeholder="*.json" v-model="input3">
        <template slot="prepend">评论数据所在目录</template>
      </el-input>
    </div>
    <div style="margin-top: 15px;">
      <el-button type="primary" @click="open1">
        上传
      </el-button>
    </div>

  </div>
</template>

<script>
function wait(ms) {
  return new Promise(resolve => setTimeout(() =>resolve(), ms));
}
export default {
  data() {
    return {
      input1: "D:/business.json",
      input2: "D:/user.json",
      input3: "D:/comment.json",
      algorithm: ""}
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

<style>
  .el-select .el-input {
    width: 130px;
  }
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
</style>