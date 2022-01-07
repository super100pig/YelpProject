<template>
  <div id="app">
    <el-container>
      <el-header style="background-color: #B3C0D1">
        <div style="font-size: x-large; color: #333; margin-top: 12px">
          <i class="el-icon-trophy"></i> 小众点评 <i class="el-icon-trophy"></i>
        </div>
        <el-row type="flex" justify="end">
          <el-col :span="6">
            <el-dropdown>
              <el-button icon="el-icon-user" round>
                欢迎登陆，点评用户star！<i class="el-icon-arrow-down el-icon--right"></i>
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
      <el-aside width="200px">
        <el-menu default-active="/uploadPage" :default-openeds="['1', '2']" class="el-menu-vertical-demo" background-color="rgb(238, 241, 246)" text-color="#333" router>
          <el-menu-item index="/notification">
              <i class="el-icon-lollipop"></i>
              <span slot="title">点评Demo</span>
            </el-menu-item>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-setting"></i>
              <span>数据预览</span>
            </template>
            <el-menu-item index="/uploadPage">
              <span slot="title">
                数据上传
              </span>
            </el-menu-item>
            <el-menu-item index="/nodeTable">
              <span slot="title">
                Yelp | 商户
              </span>
            </el-menu-item>
            <el-menu-item index="/edgeTable">
              <span slot="title">
                Yelp | 评论
              </span>
            </el-menu-item>
            <el-menu-item index="/deviceTable">
              <span slot="title">
                Yelp | 数据勘探
              </span>
            </el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-share"></i>
              <span>推荐关联</span>
            </template>
            <!-- <el-menu-item index="/structureGraph">
              <span slot="title">
                路径关联图
              </span>
            </el-menu-item> -->
            <el-menu-item index="/attributeGraph">
              <span slot="title">
                用户-商户关联
              </span>
            </el-menu-item>
            <el-menu-item index="/graph">
              <span slot="title">
                商户-用户关联
              </span>
            </el-menu-item>
            <el-menu-item index="/stationGraph">
              <span slot="title">
                全体关联
              </span>
            </el-menu-item>
          </el-submenu>
          
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
        <el-footer>© 数据挖掘第四组 2021</el-footer>
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
