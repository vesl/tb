<template>
    <PrimeCard>
        <template #title>Model <span class="text-success">{{ name }}</span> performances</template>
        <template #content>
            <div><i class="pi pi-clock mr-2"></i><span class="text-success">{{ training_time }}</span></div>
            <div class="flex flex-wrap justify-content-center">
                <div class="flex flex-auto col-4 justify-content-center">
                    <PrimeKnob v-model="f1_score" :min="0" :max="1" :step="0.01" disabled />
                    <label class="text-sm block">F1 Score</label>
                </div>
                <div class="flex flex-auto col-4 justify-content-center">
                    <PrimeKnob v-model="score" :min="0" :max="1" :step="0.01" disabled />
                    <label class="text-sm block">Score</label>
                </div>
                <div class="flex flex-auto col-4 justify-content-center">
                    <PrimeKnob v-model="accuracy" :min="0" :max="1" :step="0.01" disabled />
                    <label class="text-sm block">Accuracy</label>
                </div>
            </div>
            <PrimeChart type="line" :data="cross_val_score.data" :options="cross_val_score.options" class="h-30rem" />
            <PrimeChart type="bar" :data="confusion_matrix.data" :options="confusion_matrix.options" class="h-30rem" />
        </template>
    </PrimeCard>
</template>

<script>
export default {
    name: 'random-forest-perfs',
    props: ['perfs','name'],
    data() {
        return {
            f1_score: Number(Number.parseFloat(this.perfs.f1_score).toFixed(2)),
            score: Number(Number.parseFloat(this.perfs.score).toFixed(2)),
            accuracy: Number(Number.parseFloat(this.perfs.accuracy).toFixed(2)),
            training_time: this.perfs.training_time,
            cross_val_score: {
                data: {
                    labels: Array(this.perfs.cross_val_score.length).fill(1).map((x, y) => x + y),
                    datasets: [{data:this.perfs.cross_val_score}],
                },
                options: {maintainAspectRatio:false,plugins:{legend:{display:false}}}
            },
            confusion_matrix: {
                data: {
                    labels: ['Down','Up'],
                    datasets: [
                        {
                            label: 'Down',
                            type: 'bar',
                            backgroundColor: '#f78181',
                            data: this.perfs.confusion_matrix[0]
                        },
                        {
                            label: 'Up',
                            type: 'bar',
                            backgroundColor: '#d0f5a9',
                            data: this.perfs.confusion_matrix[1]
                        }
                    ]
                },
                options: {maintainAspectRatio:false,plugins:{legend:{display:false}}}
            }
        }
    }
}
</script>