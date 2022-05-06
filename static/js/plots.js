function init(){
    //Solution Line Graph
    async function chartdata(){
        let response = await fetch('/solutionchart')
        let allData = await response.json()
        console.log(allData.dates)

        var ph = {
            x: allData.dates,
            y: allData.ph,
            mode: 'lines+markers',
            name: 'pH',
            line: {color: '008EFF'},
            connectgaps: true,
        };
        var tds = {
            x: allData.dates,
            y: allData.tds,
            mode: 'lines+markers',
            name: 'TDS',
            line: {color: 'FF9800'},
            connectgaps: true,
            yaxis: 'y3'
        };
        var volume = {
            x: allData.dates,
            y: allData.volume,
            mode: 'lines+markers',
            name: 'Volume',
            line: {color: '7ED321'},
            connectgaps: true,
            yaxis: 'y2'
        };
        var layout = {
            title: 'Solution Readings',
            legend: {
                orientation: "h",
                valign: "top"

            },
            xaxis: {
                tickformat: '%a %e %b',
                showgrid: false                
            },
            yaxis: {
                title: 'pH',
                range: [5,8],
                position: 0,
                color: '008EFF',
                showgrid: false
            },
            yaxis2: {
                title: 'Volume (Liters)',
                overlaying: 'y',
                side: 'left',
                // anchor: 'free',
                position: .05,
                range: [6,10],
                color: '7ED321',
                showgrid: false  
            },
            yaxis3: {
                title: 'TDS (mg/L)',
                overlaying: 'y',
                side: 'right',
                color: 'FF9800',
                range:[600,1000],
                showgrid: false
            }
        };

        var allTraces=[ph,tds,volume];

        // Use Plotly to plot the data with the layout. 
        Plotly.newPlot("solution_chart",allTraces, layout)
    }

    chartdata()      

};

d3.select(window).on("load", init)