<template>
	<div class="lw-chart" ref="chartContainer"></div>
</template>

<script>
import { createChart } from 'lightweight-charts';

// Lightweight Chart instances are stored as normal JS variables
// If you need to use a ref then it is recommended that you use `shallowRef` instead
let series;
let chart;

// Function to get the correct series constructor name for current series type.
function getChartSeriesConstructorName(type) {
	return `add${type.charAt(0).toUpperCase() + type.slice(1)}Series`;
}

// Creates the chart series and sets the data.
const addSeriesAndData = (type, seriesOptions, data, markers) => {
	const seriesConstructor = getChartSeriesConstructorName(type);
	series = chart[seriesConstructor](seriesOptions);
	series.setData(data);
	if (markers) series.setMarkers(markers);
};

// Auto resizes the chart when the browser window is resized.
const resizeHandler = container => {
	if (!chart || !container) return;
	const dimensions = container.getBoundingClientRect();
	chart.resize(dimensions.width, dimensions.height);
};

export default {
	props: {
		type: {
			type: String,
			default: 'line',
		},
		data: {
			type: Array,
			required: true,
		},
		autosize: {
			default: false,
			type: Boolean,
		},
		chartOptions: {
			type: Object,
		},
		seriesOptions: {
			type: Object,
		},
		timeScaleOptions: {
			type: Object,
		},
		priceScaleOptions: {
			type: Object,
		},
		markers: {
			type: Array,
		},
	},
	mounted() {
		// Create the Lightweight Charts Instance using the container ref.
		chart = createChart(this.$refs.chartContainer, this.chartOptions);
		addSeriesAndData(this.type, this.seriesOptions, this.data, this.markers);

		if (this.priceScaleOptions) {
			chart.priceScale().applyOptions(this.priceScaleOptions);
		}

		if (this.timeScaleOptions) {
			chart.timeScale().applyOptions(this.timeScaleOptions);
		}

		chart.timeScale().fitContent();

		if (this.autosize) {
			window.addEventListener('resize', () =>
				resizeHandler(this.$refs.chartContainer)
			);
		}
	},
	unmounted() {
		if (chart) {
			chart.remove();
			chart = null;
		}
		if (series) {
			series = null;
		}
		window.removeEventListener('resize', resizeHandler);
	},
	/*
	 * Watch for changes to any of the component properties.
	 *
	 * If an options property is changed then we will apply those options
	 * on top of any existing options previously set (since we are using the
	 * `applyOptions` method).
	 *
	 * If there is a change to the chart type, then the existing series is removed
	 * and the new series is created, and assigned the data.
	 *
	 */
	watch: {
		autosize(enabled) {
			if (!enabled) {
				window.removeEventListener('resize', () =>
					resizeHandler(this.$refs.chartContainer)
				);
				return;
			}
			window.addEventListener('resize', () =>
				resizeHandler(this.$refs.chartContainer)
			);
		},
		type() {
			if (series && chart) {
				chart.removeSeries(series);
			}
			addSeriesAndData(this.type, this.seriesOptions, this.data);
		},
		data(newData) {
			if (!series) return;
			series.setData(newData);
		},
		chartOptions(newOptions) {
			if (!chart) return;
			chart.applyOptions(newOptions);
		},
		seriesOptions(newOptions) {
			if (!series) return;
			series.applyOptions(newOptions);
		},
		priceScaleOptions(newOptions) {
			if (!chart) return;
			chart.priceScale().applyOptions(newOptions);
		},
		timeScaleOptions(newOptions) {
			if (!chart) return;
			chart.timeScale().applyOptions(newOptions);
		},
	},
	methods: {
		fitContent() {
			if (!chart) return;
			chart.timeScale().fitContent();
		},
		getChart() {
			return chart;
		},
	},
	expose: ['fitContent', 'getChart'],
};
</script>

<style scoped>
.lw-chart {
	height: 300px;
	background: var(--primary);
}
</style>