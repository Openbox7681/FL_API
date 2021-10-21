fs = [f for f in os.listdir(self.model_path) if ".model.pickle.dat" in f]

for i, f in enumerate(fs):
    m_path = os.path.join(self.model_path, f)
    m = pickle.load(open(m_path, "rb"))
    