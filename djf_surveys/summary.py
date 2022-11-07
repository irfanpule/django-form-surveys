import random

from django.utils.translation import gettext

from djf_surveys import models
from djf_surveys.models import TYPE_FIELD, Survey, Question, Answer
from djf_surveys.utils import create_star


COLORS = [
  '#64748b', '#a1a1aa', '#374151', '#78716c', '#d6d3d1', '#fca5a5', '#ef4444', '#7f1d1d',
  '#fb923c', '#c2410c', '#fcd34d', '#b45309', '#fde047', '#bef264', '#ca8a04', '#65a30d',
  '#86efac', '#15803d', '#059669', '#a7f3d0', '#14b8a6', '#06b6d4', '#155e75', '#0ea5e9',
  '#075985', '#3b82f6', '#1e3a8a', '#818cf8', '#a78bfa', '#a855f7', '#6b21a8', '#c026d3',
  '#db2777', '#fda4af', '#e11d48', '#9f1239'
]

class ChartJS:
    """
    this class to generate chart https://www.chartjs.org
    """
    chart_id = ""
    chart_name = ""
    element_html = ""
    element_js = ""
    width = 400
    height = 400
    data = []
    labels = []
    colors = COLORS

    def __init__(self, chart_id: str, chart_name: str, *args, **kwargs):
        self.chart_id = f"djfChart{chart_id}"
        self.chart_name = chart_name

    def _base_element_html(self):
        self.element_html = f"""
<div class="swiper-slide">
    <blockquote class="p-6 border border-gray-100 rounded-lg shadow-lg bg-white">
      <canvas id="{self.chart_id}" width="{self.width}" height="{self.height}"></canvas>
    </blocquote>
</div>
"""

    def _shake_colors(self):
        self.colors = random.choices(COLORS, k=len(self.labels))

    def _config(self):
        pass

    def _setup(self):
        pass

    def render(self):
        self._base_element_html()
        self._shake_colors()
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
    """ this class to generate pie chart"""

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


class ChartBar(ChartJS):
    """ this class to generate bar chart"""

    def _config(self):
        script = """
const config%s = {
  type: 'bar',
  data: data%s,
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  },
};
"""
        return script % (self.chart_id, self.chart_id)

    def _setup(self):
        script = """
const data%s = {
  labels: %s,
  datasets: [{
    label: '%s',
    data: %s,
    backgroundColor: %s,
    borderWidth: 1
  }]
};
"""
        return script % (self.chart_id, self.labels, self.chart_name, self.data, self.colors)


class ChartBarRating(ChartBar):
    height = 200
    rate_avg = 0

    def _base_element_html(self):
        stars = create_star(active_star=int(self.rate_avg))
        self.element_html = f"""
<div class="swiper-slide">
    <blockquote class="p-6 border border-gray-100 rounded-lg shadow-lg bg-white">
      <div class="bg-yellow-100 space-y-1 py-5 rounded-md border border-yellow-200 text-center shadow-xs mb-2">
          <h1 class="text-5xl font-semibold"> {self.rate_avg}</h1>
          <div class="flex justify-center">
              {stars}
          </div>
          <h5 class="mb-0 mt-1 text-sm"> Rate Average</h5>
      </div>
      <canvas id="{self.chart_id}" width="{self.width}" height="{self.height}"></canvas>
    </blocquote>
</div>
"""


class SummaryResponse:

    def __init__(self, survey: Survey):
        self.survey = survey
    
    def _process_radio_type(self, question: Question) -> str:
        pie_chart = ChartPie(chart_id=f"chartpie_{question.id}", chart_name=question.label)
        labels = question.choices.split(",")
        
        data = []
        for label in labels:
            clean_label = label.strip().replace(' ', '_').lower()
            count = Answer.objects.filter(question=question, value=clean_label).count()
            data.append(count)

        pie_chart.labels = labels
        pie_chart.data = data
        return pie_chart.render()
    
    def _process_rating_type(self, question: Question):
        bar_chart = ChartBarRating(chart_id=f"chartbar_{question.id}", chart_name=question.label)
        labels = ['1', '2', '3', '4', '5']
        
        data = []
        for label in labels:
            count = Answer.objects.filter(question=question, value=label).count()
            data.append(count)

        values_rating = Answer.objects.filter(question=question).values_list('value', flat=True)
        values_convert = [int(v) for v in values_rating]
        try:
          rating_avg = round(sum(values_convert) / len(values_convert), 1)
        except ZeroDevisionError:
          rating_avg = 0
        
        bar_chart.labels = labels
        bar_chart.data = data
        bar_chart.rate_avg = rating_avg
        return bar_chart.render()

    def _process_multiselect_type(self, question: Question) -> str:
        bar_chart = ChartBar(chart_id=f"barchart_{question.id}", chart_name=question.label)
        labels = question.choices.split(",")

        str_value = []
        for answer in Answer.objects.filter(question=question):
            str_value.append(answer.value)
        all_value = ",".join(str_value)
        data_value = all_value.split(",")

        data = []
        for label in labels:
            clean_label = label.strip().replace(' ', '_').lower()
            data.append(data_value.count(clean_label))

        bar_chart.labels = labels
        bar_chart.data = data
        return bar_chart.render()

    def generate(self):
        html_str = []
        for question in self.survey.questions.all():
            if question.type_field == TYPE_FIELD.radio or question.type_field == TYPE_FIELD.select:
                html_str.append(self._process_radio_type(question))
            elif question.type_field == TYPE_FIELD.multi_select:
                html_str.append(self._process_multiselect_type(question))
            elif question.type_field == TYPE_FIELD.rating:
                html_str.append(self._process_rating_type(question))
        if not html_str:
            input_types = ', '.join(str(x[1]) for x in models.Question.TYPE_FIELD if
                      x[0] in (models.TYPE_FIELD.radio, models.TYPE_FIELD.select, models.TYPE_FIELD.multi_select, models.TYPE_FIELD.rating))
            return """
<div class="bg-yellow-100 space-y-1 py-5 rounded-md border border-yellow-200 text-center shadow-xs mb-2">
    <h1 class="text-2xl font-semibold">{}</h1>
    <h5 class="mb-0 mt-1 text-sm p-2">{}</h5>
</div>
""".format(gettext("No summary"), gettext("Summary is available only for input type: %(input_types)s") % dict(input_types=input_types))

        return " ".join(html_str)
