from flask import Flask, request, jsonify
from modsim import *
from pandas import *

app = Flask(__name__)

# Model

class Mymodel:
    def __init__(self):
        self.data = read_csv('data/World_population_estimates.csv')
        self.data.index = self.data.Year
        self.census = self.data.census / 1e9
        self.un = self.data.un / 1e9
        self.maddi = self.data.maddison / 1e9
        self.worldometer = self.data.worldometers / 1e9

    def initialize_system_default(self, startYear, endYear, startingPopulation):
        system = System(startYear=startYear,
                        endYear=endYear,
                        startingPopulation=startingPopulation,
                        alpha=0.025,
                        beta=-0.0018)
        return system

    def initialize_system(self, startYear, endYear, startingPopulation, alpha, beta):
        system = System(startYear=startYear,
                        endYear=endYear,
                        startingPopulation=startingPopulation,
                        alpha=alpha,
                        beta=beta)
        return system

    def update_func_quad(self, pop, t, system):
        """Update population based on a quadratic model.

        pop: current population in billions
        t: what year it is
        system: system object with model parameters
        """
        net_growth = system.alpha * pop + system.beta * pop ** 2
        return pop + net_growth

    # run_simulation takes the update
    # function as a parameter and calls it just like any other function.
    def run_simulation(self, system, update_func):
        """Simulate the system using any update function.
        system: System object
        update_func: function that computes the population next year
        returns: TimeSeries
        """
        results = TimeSeries()
        results[system.startYear] = system.startingPopulation

        for t in linrange(system.startYear, system.endYear):
            results[t + 1] = update_func(results[t], t, system)

        return results

    def get_year(self, startYear, endYear):
        year_list = list()
        end = int(endYear + 1)
        for x in range(int(startYear), end):
            year_list.append(x)
        return year_list

    def get_year_un(self):
        year_list = list()
        for year in range(2020, 2105, 5):
            year_list.append(year)
        return year_list

    def get_net_growth_dic(self, system, results):
        growth = {}

        cencus_list = compute_rel_diff(self.census)
        cencus_list = cencus_list.dropna().tolist()

        # un_list = compute_rel_diff(self.un).dropna().tolist()
        maddi_list = compute_rel_diff(self.maddi).dropna().tolist()
        worldometer_list = compute_rel_diff(self.worldometer).dropna().tolist()
        predictions_list = compute_rel_diff(results).dropna().tolist()

        cencus_dic = {}
        cencus_dic['year'] = self.get_year(1951, 2050)
        cencus_dic['pop'] = cencus_list

        maddi_dic = {}
        maddi_dic['year'] = self.get_year(1951, 2009)
        maddi_dic['pop'] = maddi_list

        world_dic = {}
        world_dic['year'] = self.get_year(1951, 2100)
        world_dic['pop'] = worldometer_list

        predictions_dic = {}
        predictions_dic['year'] = self.get_year(system.startYear, system.endYear)
        predictions_dic['pop'] = predictions_list

        # cencus_dic = dict(zip(self.get_year(1950, 2050), cencus_list))
        #
        # # un_dic = dict(zip(self.get_year(1950, 2016), un_list))
        # # un_dic_2 = dict(zip(self.get_year_un(), un_list[67:]))
        # # un_dic.update(un_dic_2)
        #
        # maddi_dic = dict(zip(self.get_year(1950, 2009), maddi_list))
        # predictions_dic = dict(zip(self.get_year(system.startYear, system.endYear), predictions_list))
        # world_dic = dict(zip(self.get_year(1951, 2100), worldometer_list))

        growth['cencus'] = cencus_dic
        growth['maddi'] = maddi_dic
        growth['worldometer'] = world_dic
        growth['predictions'] = predictions_dic
        return growth

    def get_data_dic(self, system, results):
        data = {}
        # data['cencus'] = self.census.dropna().tolist()
        # data['un'] = self.un.dropna().tolist()
        # data['maddi'] = self.maddi.dropna().tolist()
        # data['worldometer'] = self.worldometer.dropna().tolist()
        # data['predictions'] = results.dropna().tolist()
        cencus_list = self.census.dropna().tolist()
        un_list = self.un.dropna().tolist()
        maddi_list = self.maddi.dropna().tolist()
        worldometer_list = self.worldometer.dropna().tolist()
        predictions_list = results.dropna().tolist()

        # self.get_year(1950, 2050)
        # dict(zip(self.get_year(1950, 2050), cencus_list))
        cencus_dic = {}
        cencus_dic['year'] = self.get_year(1950, 2050)
        cencus_dic['pop'] = cencus_list

        un_dic = {}
        un_dic['year'] = self.get_year(1950, 2016) + self.get_year_un()
        un_dic['pop'] = un_list

        maddi_dic = {}
        maddi_dic['year'] = self.get_year(1950, 2009)
        maddi_dic['pop'] = maddi_list

        world_dic = {}
        world_dic['year'] = self.get_year(1951, 2100)
        world_dic['pop'] = worldometer_list

        predictions_dic = {}
        predictions_dic['year'] = self.get_year(system.startYear, system.endYear)
        predictions_dic['pop'] = predictions_list

        # un_dic = dict(zip(self.get_year(1950, 2016), un_list))
        # un_dic_2 = dict(zip(self.get_year_un(), un_list[67:]))
        # un_dic.update(un_dic_2)

        # maddi_dic = dict(zip(self.get_year(1950, 2009), maddi_list))
        # predictions_dic = dict(zip(self.get_year(system.startYear, system.endYear), predictions_list))
        # world_dic = dict(zip(self.get_year(1951, 2100), worldometer_list))

        data['cencus'] = cencus_dic
        data['un'] = un_dic
        data['maddi'] = maddi_dic
        data['worldometer'] = world_dic
        data['predictions'] = predictions_dic
        return data


app = Flask(__name__)
model = Mymodel()


@app.route("/predict", methods=['POST'])
def predict():
    staring_year = int(request.json['start_year'])
    ending_year = int(request.json['end_year'])
    staring_pop = float(request.json['start_pop'])
    alpha = float(request.json['alpha'])
    beta = float(request.json['beta'])

    print(request.json)

    staring_pop = staring_pop / 1e9

    if alpha == 0.025 and beta == -0.0018:
        system = model.initialize_system_default(staring_year, ending_year, staring_pop)
        results = model.run_simulation(system, model.update_func_quad)
        main_dict = {}
        main_dict['data'] = model.get_data_dic(system, results)
        main_dict['netgrowth'] = model.get_net_growth_dic(system, results)
        return jsonify(main_dict)

    # t_0 = 2.557629e+09 / 1e9
    system = model.initialize_system(staring_year, ending_year, staring_pop, alpha, beta)
    results = model.run_simulation(system, model.update_func_quad)
    main_dict = {}
    main_dict['data'] = model.get_data_dic(system, results)
    main_dict['netgrowth'] = model.get_net_growth_dic(system, results)
    return jsonify(main_dict)



@app.route("/test", methods=['GET'])
def test():
    return "Hello world"


if __name__ == '__main__':
	app.run()

