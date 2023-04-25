import { createRouter, createWebHashHistory } from 'vue-router'

import test from '@/views/test.vue'
import test2 from '@/views/test2.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            component: test
        },
        {
            path: '/scrapper/klines',
            component: test2
        },
        {
            path: '/plotter/datasets',
            component: test
        }
    ]
})

export default router;