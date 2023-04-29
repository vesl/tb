import { createRouter, createWebHashHistory } from 'vue-router'

import Content from '@/components/organisms/Content.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/:app/:view',
            component: Content
        },
    ]
})

export default router;