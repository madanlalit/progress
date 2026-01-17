class Progress < Formula
  include Language::Python::Virtualenv

  desc "Beautiful year calendar wallpapers showing yearly progress"
  homepage "https://github.com/madanlalit/progress"
  url "https://github.com/madanlalit/progress/archive/v1.2.0.tar.gz"
  sha256 "8cbe3de9eb0e76f362fd3d29a66db91eb0309830e322173d5fa0399c8de000e1"
  license "MIT"

  depends_on "pillow"
  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources(system_site_packages: true)
  end

  # Automatic daily update service
  service do
    run [opt_bin/"progress", "generate", "--output", "#{Dir.home}/.progress/wallpaper.png"]
    run_type :cron
    cron "1 0 * * *" # Run daily at 00:01
    keep_alive false
    working_dir Dir.home
    log_path var/"log/progress.log"
    error_log_path var/"log/progress.error.log"
  end

  def caveats
    <<~EOS
      ✨ Progress installed successfully!

      To start the automatic daily wallpaper updater:
        brew services start progress

      To generate a wallpaper manually right now:
        progress generate

      The wallpaper will update daily at 00:01 and be saved to ~/.progress/wallpaper.png
    EOS
  end

  test do
    system bin/"progress", "--version"
    system bin/"progress", "generate", "--no-set", "--mode", "day"
  end
end
