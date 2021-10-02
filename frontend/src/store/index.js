import AuthStore from './auth-store/AuthStore';
import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoading: false,
    feeds: null
  },
  mutations: {
    setLoadingState(state) {
      state.isLoading = !state.isLoading
    },
    setFeeds(state, feeds) {
      state.feeds = feeds;
    }
  },
  actions: {
    setFeedsOnLoad(context, feeds) {
      context.commit('setFeeds', feeds)
    }
  },
  modules: {
    auth: AuthStore
  }
})
