<script>
// Contains the different dropdown menus for ergonomists and users
import User from '../components/User.vue'
import Ergonomist from '../components/Ergonomist.vue'

export default {
  components: {
    User,
    Ergonomist
  },
  data() {
    return {
      showDropdown: false,
      user: null
    }
  },
  methods: {
    logOut() {
      localStorage.removeItem('user')
      this.$router.push('/')
    },
    hide() {
      if (this.showDropdown) {
        this.showDropdown = false
      }
    }
  },

  created() {
    if (!localStorage.getItem("user")) {
      this.$router.push('/')
    } else {
      this.user = JSON.parse(localStorage.getItem("user"))
    }
  }
}
</script>

<template>
  <header>
    <span class="title">ErgoSmart</span>
    <div class="profile">
      <!-- svelte-ignore a11y-missing-attribute -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <a v-on:click="showDropdown = !showDropdown">
        <i class="fas fa-user fa-fw"></i>
        <span>{{ user?.email }}</span></a>
    </div>
    <ul v-click-outside="hide" v-if="showDropdown" class="dropdown">
      <li v-on:click="logOut()" class="drop-down-item">Logout</li>
    </ul>
  </header>
  <template v-if="user && user.role === 'USER'">
    <User />
  </template>
  <template v-if="user && user.role === 'ERGONOMIST'">
    <Ergonomist />
  </template>
</template>

<style scoped>
header {
  width: 100%;
  height: 70px;
  background-color: #343a40;
  box-sizing: border-box;
  padding: 0 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile {
  color: rgba(255, 255, 255, 0.5);
  font-size: 20px;
}

.profile a:hover {
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
}

a::after {
  display: inline-block;
  margin-left: 0.255em;
  vertical-align: 0.255em;
  content: "";
  border-top: 0.3em solid;
  border-right: 0.3em solid transparent;
  border-bottom: 0;
  border-left: 0.3em solid transparent;
}

.dropdown {
  position: absolute;
  top: 60px;
  right: 60px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  background-color: #fff;
  z-index: 999;
}

.drop-down-item {
  display: block;
  width: 100%;
  padding: 16px 24px;
  box-sizing: border-box;
}

.drop-down-item:hover {
  background-color: #f8f9fa;
  cursor: pointer;
}

.title {
  color: rgba(255, 255, 255, 0.5);
  font-size: 25px;
}
</style>
