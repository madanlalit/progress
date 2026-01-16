class Progress < Formula
  include Language::Python::Virtualenv

  desc "Beautiful year calendar wallpapers showing yearly progress"
  homepage "https://github.com/madanlalit/progress"
  url "https://github.com/madanlalit/progress/archive/v1.0.0.tar.gz"
  sha256 "3782f582f7eca7dacd15ab8dc800f492eb1bc4593b1cbd6ef5b85fb731c12075"
  license "MIT"

  depends_on "python@3.11"

  resource "Pillow" do
    url "https://files.pythonhosted.org/packages/cd/74/ad3d526f3bf7b6d3f408b73fde271ec69dfac8b81341a318ce825f2b3812/pillow-10.4.0.tar.gz"
    sha256 "166c1cd4d24309b30d61f79f4a9114b7b2313d7450912277855ff5dfd7cd4a06"
  end

  def install
    virtualenv_install_with_resources
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
    system bin/"progress", "generate", "--no-set", "--mode", "week"
  end
end
