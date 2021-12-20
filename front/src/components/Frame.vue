<template>
  <div id="app">
    <el-container>
      <el-header style="background-color: midnightblue" height="80px">
        <el-row>
          <div style="font-size: xx-large; color: white; font-family: 幼圆,serif">西门子零件异常检测</div>
        </el-row>
        <el-row type="flex" justify="end">
          <el-col :span="6">
            <el-dropdown>
              <el-button icon="el-icon-user" round>
                欢迎登陆，王小明！<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>设置</el-dropdown-item>
                <el-dropdown-item>切换账号</el-dropdown-item>
                <el-dropdown-item>注销</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-col>
        </el-row>

      </el-header>
    </el-container>
    <el-container>
      <el-aside style="background-color: #545c64">
        <el-menu default-active="/uploadPage" :default-openeds="['1', '2']" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" router>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>数据上传与预览</span>
            </template>
            <el-menu-item index="/uploadPage">
              <span slot="title">
                数据上传
              </span>
            </el-menu-item>
            <el-menu-item index="/nodeTable">
              <span slot="title">
                零件数据
              </span>
            </el-menu-item>
            <el-menu-item index="/edgeTable">
              <span slot="title">
                零件关联数据
              </span>
            </el-menu-item>
            <el-menu-item index="/deviceTable">
              <span slot="title">
                设备数据
              </span>
            </el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>质量追溯</span>
            </template>
            <el-menu-item index="/structureGraph">
              <span slot="title">
                路径关联图
              </span>
            </el-menu-item>
            <el-menu-item index="/attributeGraph">
              <span slot="title">
                属性关联图
              </span>
            </el-menu-item>
            <el-menu-item index="/graph">
              <span slot="title">
                多信息关联图
              </span>
            </el-menu-item>
            <el-menu-item index="/stationGraph">
              <span slot="title">
                工件设备图
              </span>
            </el-menu-item>
          </el-submenu>
          <el-menu-item index="/notification">
            <i class="el-icon-setting"></i>
            <span slot="title">
              故障检测
            </span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
        <el-footer>© 西门子（中国）有限公司 1996 – 2020</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>

export default {
  name: 'frame'
}
</script>

<style>
</style>
