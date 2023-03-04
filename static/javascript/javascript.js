let contestData = JSON.parse( document.getElementById('contest_results').textContent )

const canvas = document.getElementById('result-chart').getContext('2d');


var csGradient = canvas.createLinearGradient(0 , 0 , 0 , 200);
csGradient.addColorStop(0 , "rgba(58,123,213,1)");
csGradient.addColorStop(1 , 'rgba(0,210,255,1)' );

var ratingChanges = []
var ratingChangesOverContest = []
var titleChanges = []
var contestsName = []
var lables = []

for(let i = 0; i < contestData.length; i++){
    lables.push('');
    ratingChangesOverContest.push( contestData[i].rating_change )
    ratingChanges.push(contestData[i].new_rating)
    titleChanges.push(contestData[i].title_change)
    contestsName.push(contestData[i].name)
}

const contestChartData = {
    labels : lables,
    datasets: [
        {
            label : "Contest result",
            data : ratingChanges,
            fill : true,
            backgroundColor : csGradient,
            pointBackgroundColor: 'rgba(58,123,213,1)',
            pointBorderColor : 'rgba(255,255,255,1)',
        }
    ]
}

const contestChartConfig = {
    type: 'line',
    data: contestChartData,
    options: {
        responsive : true,
        hoverRadius: 10,
        scales: {
            y: {
                type: 'linear'
            }
        },
        plugins : {
            tooltip : {
                callbacks: {
                    label : (context) => {
                        return `${contestsName[context.dataIndex]}, New rating: ${ratingChanges[context.dataIndex]}`;
                    }
                }
            }
        }
    }
}

contestChart = new Chart(
    canvas,
    contestChartConfig
)

