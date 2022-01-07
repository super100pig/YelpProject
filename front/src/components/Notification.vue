<template>
  <div>
    <h2>Amici’s East Coast Pizzeria</h2>
    <img src="../img/pizza.jpg" alt="1" style="width: 500px"/>
    <el-row>
      <el-col :span="4">
        <el-row type="flex" justify="end" align="middle"><p>推荐指数：</p></el-row>
      </el-col>
      <el-col :span="20"><el-rate :value="4" disabled show-score score-template="{value}星"></el-rate></el-col>
    </el-row>

    <el-row>
      <el-col :span="12">
      <h3>评论区</h3>
      <el-row class="comment-area">
          <el-row :gutter="20">
            <el-col :span="4">
              <el-row type="flex" justify="end" align="middle"><img src="../img/user-64.png" alt="1"/></el-row>
            </el-col>
            <el-col :span="20">
              <el-row type="flex" justify="start" align="middle">
                <el-link>Alice Wu</el-link><el-tag type="warning">SVIP</el-tag>
              </el-row>
              <el-row type="flex" justify="start" align="middle">
                <el-rate :value="4" disabled show-score score-template="{value}星"></el-rate>
              </el-row>
              <p>
                Apparently Prides Osteria had a rough summer as evidenced by the almost empty dining room at 6:30 on a Friday night. <br/>However new blood in the kitchen seems to have revitalized the food from other customers recent visits. Waitstaff was warm but unobtrusive.
              </p>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="4">
              <el-row type="flex" justify="end" align="middle"><img src="../img/user-64.png" alt="1"/></el-row>
            </el-col>
            <el-col :span="20">
              <el-row type="flex" justify="start" align="middle">
                <el-link>Jack Ma</el-link><el-tag type="warning">SVIP</el-tag>
              </el-row>
              <el-row type="flex" justify="start" align="middle">
                <el-rate :value="2" disabled show-score score-template="{value}星"></el-rate>
              </el-row>
              <p>
                I've stayed at many Marriott and Renaissance Marriott's and this was a huge disappointment! The front desk and atrium is nice..there is a starbucks on site which is nice.<br/>The rooms are run down and old. There is a flat screen but that is to be expected of a Renaissance.
              </p>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="4">
              <el-row type="flex" justify="end" align="middle"><img src="../img/user-64.png" alt="1"/></el-row>
            </el-col>
            <el-col :span="20">
              <el-row type="flex" justify="start" align="middle">
                <el-link>Sicong Wang</el-link><el-tag type="warning">SVIP</el-tag>
              </el-row>
              <el-row type="flex" justify="start" align="middle">
                <el-rate :value="5" disabled show-score score-template="{value}星"></el-rate>
              </el-row>
              <p>
                The food is always great here. The service from both the manager as well as the staff is super. Only draw back of this restaurant is it's super loud. If you can, snag a patio table!
              </p>
            </el-col>
          </el-row>
      </el-row>
      </el-col>
      <el-col :span="12">
        <h3>相关推荐</h3>
        <h4>Bun Me Up</h4>
        <img src="../img/res1.jpeg" alt="1" style="width: 200px; height: 150px; object-fit: cover"/>
        <el-row>
          <el-col :span="4">
            <el-row type="flex" justify="end" align="middle"><p>推荐指数：</p></el-row>
          </el-col>
          <el-col :span="20"><el-rate :value="4" disabled show-score score-template="{value}星"></el-rate></el-col>
        </el-row>
        <h4>Jane Ellen Bakery</h4>
        <img src="../img/res2.jpeg" alt="1" style="width: 200px; height: 150px; object-fit: cover"/>
        <el-row>
          <el-col :span="4">
            <el-row type="flex" justify="end" align="middle"><p>推荐指数：</p></el-row>
          </el-col>
          <el-col :span="20"><el-rate :value="4" disabled show-score score-template="{value}星"></el-rate></el-col>
        </el-row>
        <h4>Nick The Greek</h4>
        <img src="../img/res3.jpeg" alt="1" style="width: 200px; height: 150px; object-fit: cover"/>
        <el-row>
          <el-col :span="4">
            <el-row type="flex" justify="end" align="middle"><p>推荐指数：</p></el-row>
          </el-col>
          <el-col :span="20"><el-rate :value="4" disabled show-score score-template="{value}星"></el-rate></el-col>
        </el-row>
      </el-col>
    </el-row>
    <h3>去过 Amici’s East Coast Pizzeria ？给大家分享体验！</h3>
    <el-row>
      <el-row :gutter="20">
        <el-col :span="2">
          <el-row type="flex" justify="end" align="middle"><img src="../img/user-64.png" alt="1"/></el-row>
        </el-col>
        <el-col :span="10">
          <el-row type="flex" justify="start" align="middle">
            <el-link>Tony Pan</el-link><el-tag type="warning">SVIP</el-tag>
          </el-row>
          <el-row type="flex" justify="start" align="middle">
            <el-col :span="9">
              <el-rate v-model="star_rate" show-score score-template="{value}星"></el-rate>
            </el-col>
            <el-col :span="15">
              <el-row><el-button @click="getScore">让我猜猜你打几颗星？</el-button></el-row>
              <el-row><img src="../img/duck-thinking.png" style="width: 90px;"/></el-row>
            </el-col>
          </el-row>
          <el-row>
            <el-col>
              <el-input type="textarea" :rows="3" placeholder="请输入你的评价……" v-model="textarea"></el-input>
              <el-button type="primary" @click="postComment">发表</el-button>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-row>
  </div>
</template>

<script>

// function wait(ms) {
//   return new Promise(resolve => setTimeout(() =>resolve(), ms));
// }
export default {
  data() {
    return {
      textarea: "",
      star_rate: 0
    }
  },
  mounted() {
    this.show_algorithm()
  },
  methods: {
    star_press(co) {
      console.log(co);
      for (let i = 1; i <= co; i++) {
        document.getElementsByName("star" + i)[0].className="fa fa-star";
      }
      for (let i = co + 1; i <= 5; i++) {
        document.getElementsByName("star" + i)[0].className="fa fa-star-o";
      }
      document.getElementsByName("comment_score")[0].innerText = co+"分";
    },
    show_algorithm() {
      this.$axios
          .get("http://" + localStorage.getItem('backend_host') + "/get_algorithms/",{
        params: {
          text: this.textarea,
        }
      }).then(response => {
            this.tableData = response.data.score;
            console.log(this.tableData);
          });
    },
    getScore() {
      this.$message('算法正在执行……');
      console.log(this.textarea);
      this.$axios
          .get("http://" + localStorage.getItem('backend_host') + "/get_score/",{
            params: {
              text: this.textarea,
            }
          })
          .then(response => {
            this.star_rate = response.data.score;
            console.log(this.star_rate);
          });
    },
    postComment() {
      this.$message('评论发表成功！');
    }
  }
}
</script>