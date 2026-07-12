import matplotlib.pyplot as plt
def main():

    def plot_barchat(X_axis,y_axis,label_var,title_var):
        plt.Figure(figsize=(10,6),dpi=300)
        plt.bar(X_axis,y_axis,color="green",label=label_var,)
        plt.xlabel('Category')
        plt.ylabel('Range')
        plt.title(title_var)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.legend()
        plt.show()
    def box_plot(X_var,title_var='Graph',lable='data'):
        plt.figure(figsize=(5,3),dpi=200)
        plt.style.use("default")
        plt.boxplot(X_var,label=lable)
        plt.title(title_var)
        plt.legend(loc="upper right",fontsize=8)
        plt.show()


if __name__ == "__main__":
    main()
