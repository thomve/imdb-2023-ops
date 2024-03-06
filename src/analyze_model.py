import matplotlib.pyplot as plt
import xgboost as xgb



def plot_feature_importance(model: xgb.Booster):
    xgb.plot_importance(model)
    plt.show()

def plot_force_plot_instance():
    pass

def plot_force_plot():
    pass

def plot_shap_dependence_plot():
    pass


if __name__ == "__main__":
    bst = xgb.Booster()
    bst.load_model("output/xgb.json")
    plot_feature_importance(bst)
