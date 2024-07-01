import stillCenter
import AppStore

if __name__ == "__main__":
    AppStore.refresh_app_store()

    app = stillCenter.StillCenter()
    app.run()
    