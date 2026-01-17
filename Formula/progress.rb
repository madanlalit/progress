class Progress < Formula
  include Language::Python::Virtualenv

  desc "Beautiful year calendar wallpapers showing yearly progress"
  homepage "https://github.com/madanlalit/progress"
  url "https://github.com/madanlalit/progress/archive/v1.1.0.tar.gz"
  sha256 "ddea441602b99069eb8ed440f8227f7ce74676ee9176f067072da5c0ee7fedd3"
  license "MIT"

  depends_on "pillow"
  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources(system_site_packages: true)
  end

  # Automatic daily update service
  service do
    run [opt_bin/"progress", "generate", "--output", "#{Dir.home}/.progress/wallpaper.png"]
    run_type :interval
    interval 43200 # Run every 12 hours
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

      The wallpaper will be saved to ~/.progress/wallpaper.png
    EOS
  end

  test do
    system bin/"progress", "--version"
    system bin/"progress", "generate", "--no-set", "--mode", "day"
  end
end
