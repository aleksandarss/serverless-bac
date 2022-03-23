import { createApp } from 'vue';
import App from './App.vue';
import AmplifyVue from '@aws-amplify/ui-vue';
import Amplify from 'aws-amplify'
import router from './router'
import store from './store'

Amplify.configure({
    Auth: {
      region: 'us-east-1',
      userPoolId: 'us-east-1_s6UdkYeBe',
      userPoolWebClientId: '4vpprjd6p4nm4pr0g5frahls62',
      mandatorySignIn: true
    }
});

const app = createApp(App);
app.use(AmplifyVue);
app.use(store)
app.use(router);
app.mount('#app');
