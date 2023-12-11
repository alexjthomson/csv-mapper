function updateChart(chart, json, animate) {
    if (chart == null || json == null) return false;
    const datasetCount = json.data.datasets.length;
    const visibility = [];
    chart.data.datasets.forEach((_dataset, index) => {
        visibility[index] = chart.getDatasetMeta(index).hidden ?? false;
    });
    chart.data = json.data;
    chart.data.datasets.forEach((_dataset, index) => {
        if (index < visibility.length) {
            const meta = chart.getDatasetMeta(index);
            meta.hidden = visibility[index]
        }
    });
    json.options['animation'] = { duration: animate ? 1000 : 0 };
    json.options['maintainAspectRatio'] = false;
    if (!('plugins' in json.options)) {
        json.options['plugins'] = {};
    }
    json.options['plugins']['legend'] = { display: datasetCount > 1 };
    json.options['plugins']['tooltip'] = { enabled: datasetCount > 0 && json.data.datasets[0].data.length <= 2500 };
    chart.options = json.options;
    chart.update();
    return true;
}