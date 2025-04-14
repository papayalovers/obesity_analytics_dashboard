import streamlit as st
import optuna
import plotly.graph_objects as go
import optuna.visualization as vis

def main():
    # load study dari database sqlite
    study_name = "my_study_v1"  
    storage_name = "sqlite:///optuna_study.db"
    study = optuna.load_study(study_name=study_name, storage=storage_name)

    st.markdown('<center><h4>Optuna Hyperparameter Optimization Dashboard</h4></center>', unsafe_allow_html=True)

    # tampilkan best trial
    st.write(f"**Best trial value:** {study.best_trial.value}")
    st.write(f"**Best hyperparameters:** {study.best_trial.params}")

    # plot history optimasi
    fig_history = vis.plot_optimization_history(study)
    st.plotly_chart(fig_history)

    # plot parameter importance
    fig_importance = vis.plot_param_importances(study)
    st.plotly_chart(fig_importance)

    # plot slice plot
    fig_slice = vis.plot_slice(study)
    st.plotly_chart(fig_slice)


if __name__ == "__main__":
    main()
