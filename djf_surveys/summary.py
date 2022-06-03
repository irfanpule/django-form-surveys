from djf_surveys.models import TYPE_FIELD, Survey, Question, Answer


class ChartJS:
    chart_id = ""
    chart_name = ""
    element_html = ""
    element_js = ""
    width = 400
    height = 400
    data = []
    labels = []

    def __init__(self, chart_id: str, chart_name: str, *args, **kwargs):
        self.chart_id = f"djfChart{chart_id}"
        self.chart_name = chart_name
        self.element_html = f'<canvas id="{self.chart_id}" width="{self.width}" height="{self.height}"></canvas>'

    def _config(self):
        pass

    def _setup(self):
        pass

    def render(self):
        script = f"""
{self.element_html}
<script>
{self._setup()}
{self._config()}
  const myChart{self.chart_id} = new Chart(
    document.getElementById('{self.chart_id}'),
    config{self.chart_id}
  );
</script>
"""
        return script


class ChartPie(ChartJS):
    colors = [
      '#4dc9f6',
      '#f67019',
      '#f53794',
      '#537bc4',
      '#acc236'
    ]

    def _config(self):
        script = """
const config%s = {
  type: 'pie',
  data: data%s,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '%s'
      }
    }
  },
};
"""
        return script % (self.chart_id, self.chart_id, self.chart_name)

    def _setup(self):
        script = """
const data%s = {
  labels: %s,
  datasets: [
    {
      label: 'Dataset 1',
      data: %s,
      backgroundColor: %s
    }
  ]
};
"""
        return script % (self.chart_id, self.labels, self.data, self.colors)


class SummaryResponse:

    def __init__(self, survey: Survey):
        self.survey = survey
    
    def _process_radio_type(self, question: Question) -> str:
        chart_pie = ChartPie(chart_id=f"chartpie_{question.id}", chart_name=question.label)
        labels = question.choices.split(",")
        data = []
        for label in labels:
            print(label.strip().lower())
            count = Answer.objects.filter(question=question, value=label.strip().lower()).count()
            data.append(count)

        chart_pie.labels = labels
        chart_pie.data = data
        return chart_pie.render()
    
    def _process_select_type(self):
        pass

    def _process_multiselect_type(self):
        pass

    def generate(self):
        html_str = []
        for question in self.survey.questions.all():
            if question.type_field == TYPE_FIELD.radio or question.type_field == TYPE_FIELD.select:
                html_str.append(self._process_radio_type(question))
                # TODO: 
        return " ".join(html_str)
