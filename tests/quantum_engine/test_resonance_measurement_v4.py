"""
Test Suite for Resonance Measurement v4.0

This comprehensive test suite validates all resonance measurement functionality,
including quantum resonance analysis, frequency domain processing, and consciousness
enhancement.

Test Coverage:
- Resonance analysis and detection
- Frequency domain processing and analysis
- Quantum coherence and phase alignment
- Consciousness-enhanced resonance measurement
- Performance optimization and caching
- Error handling and edge cases
- Integration with quantum engine and consciousness protocol
"""

import pytest
import numpy as np
import sys
import os
import json
from datetime import datetime
import warnings

# Add quantum engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.github', 'quantum-engine'))

try:
    from resonance_measurement_v4 import (
        QuantumResonanceMeasurementV4,
        ResonanceState,
        FrequencyAnalysis,
        ResonanceMetrics,
        ResonanceType,
        FrequencyDomain,
        ResonanceMeasurementType
    )
    from unified_field_engine_v4 import ConsciousnessLevel
except ImportError as e:
    pytest.skip(f"Resonance measurement not available: {e}", allow_module_level=True)

class TestQuantumResonanceMeasurementV4:
    """Test suite for QuantumResonanceMeasurementV4 class"""
    
    @pytest.fixture
    def resonance_alpha(self):
        """Create alpha level resonance measurement for testing"""
        return QuantumResonanceMeasurementV4(
            sample_rate=22050,
            fft_size=2048,
            consciousness_level=ConsciousnessLevel.ALPHA
        )
    
    @pytest.fixture
    def resonance_gamma(self):
        """Create gamma level resonance measurement for testing"""
        return QuantumResonanceMeasurementV4(
            sample_rate=44100,
            fft_size=4096,
            consciousness_level=ConsciousnessLevel.GAMMA
        )
    
    @pytest.fixture
    def test_signal(self):
        """Create test signal for resonance analysis"""
        # Create composite signal with multiple frequencies
        sample_rate = 44100
        duration = 1.0  # 1 second
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Fundamental frequency (440 Hz)
        fundamental = np.sin(2 * np.pi * 440 * t)
        
        # Harmonics
        harmonic2 = 0.5 * np.sin(2 * np.pi * 880 * t)
        harmonic3 = 0.25 * np.sin(2 * np.pi * 1320 * t)
        
        # Noise
        noise = 0.1 * np.random.normal(0, 1, len(t))
        
        # Combine
        signal = fundamental + harmonic2 + harmonic3 + noise
        
        return signal
    
    def test_resonance_measurement_initialization(self, resonance_alpha):
        """Test quantum resonance measurement initialization"""
        assert resonance_alpha.sample_rate == 22050
        assert resonance_alpha.fft_size == 2048
        assert resonance_alpha.consciousness_level == ConsciousnessLevel.ALPHA
        
        # Check frequency parameters
        assert resonance_alpha.frequency_resolution == 22050 / 2048
        assert resonance_alpha.nyquist_frequency == 22050 / 2.0
        
        # Check performance multiplier
        assert resonance_alpha.performance_multiplier == 2.0  # Alpha multiplier
        
        # Check quantum systems are initialized
        assert resonance_alpha.quantum_field is not None
        assert resonance_alpha.consciousness_protocol is not None
        
        # Check initial state
        assert len(resonance_alpha.resonance_history) == 0
        assert isinstance(resonance_alpha.measurement_cache, dict)
    
    def test_consciousness_level_multipliers(self):
        """Test performance multipliers for different consciousness levels"""
        multipliers = {
            ConsciousnessLevel.ALPHA: 2.0,
            ConsciousnessLevel.BETA: 5.0,
            ConsciousnessLevel.GAMMA: 12.5,
            ConsciousnessLevel.DELTA: 31.25,
            ConsciousnessLevel.OMEGA: 78.125
        }
        
        for level, expected_multiplier in multipliers.items():
            resonance = QuantumResonanceMeasurementV4(
                sample_rate=44100,
                fft_size=2048,
                consciousness_level=level
            )
            assert resonance.performance_multiplier == expected_multiplier
    
    def test_analyze_quantum_resonance(self, resonance_gamma, test_signal):
        """Test quantum resonance analysis"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal,
            domain=FrequencyDomain.FREQUENCY,
            consciousness_enhancement=True
        )
        
        # Check resonance state properties
        assert isinstance(resonance_state, ResonanceState)
        assert resonance_state.consciousness_level == ConsciousnessLevel.GAMMA
        assert len(resonance_state.frequency_spectrum) == 4096
        assert len(resonance_state.amplitudes) == 4096
        assert len(resonance_state.phases) == 4096
        
        # Check metrics ranges
        assert 0.0 <= resonance_state.coherence <= 1.0
        assert 0.0 <= resonance_state.resonance_strength <= 1.0
        assert resonance_state.quality_factor >= 1.0
        
        # Check quantum state
        assert resonance_state.quantum_state is not None
        assert len(resonance_state.quantum_state) == 256  # Fixed quantum state size
        
        # Check history updates
        assert len(resonance_gamma.resonance_history) == 1
    
    def test_frequency_domain_analysis(self, resonance_gamma, test_signal):
        """Test analysis in different frequency domains"""
        domains = [
            FrequencyDomain.TIME,
            FrequencyDomain.FREQUENCY,
            FrequencyDomain.WAVELET,
            FrequencyDomain.QUANTUM,
            FrequencyDomain.CONSCIOUSNESS
        ]
        
        for domain in domains:
            resonance_state = resonance_gamma.analyze_quantum_resonance(
                signal_data=test_signal,
                domain=domain,
                consciousness_enhancement=False
            )
            
            # Check resonance state is valid
            assert resonance_state is not None
            assert len(resonance_state.frequency_spectrum) > 0
            assert len(resonance_state.amplitudes) > 0
            assert len(resonance_state.phases) > 0
    
    def test_consciousness_enhancement(self, resonance_gamma, test_signal):
        """Test consciousness enhancement of resonance analysis"""
        # Test without consciousness enhancement
        resonance_no_enhancement = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal,
            consciousness_enhancement=False
        )
        
        # Test with consciousness enhancement
        resonance_with_enhancement = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal,
            consciousness_enhancement=True
        )
        
        # Both should be valid
        assert resonance_no_enhancement is not None
        assert resonance_with_enhancement is not None
        
        # Consciousness enhancement should affect results
        assert resonance_no_enhancement.resonance_strength != resonance_with_enhancement.resonance_strength or \
               resonance_no_enhancement.coherence != resonance_with_enhancement.coherence
    
    def test_frequency_analysis(self, resonance_gamma, test_signal):
        """Test comprehensive frequency analysis"""
        # Analyze resonance first
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Perform frequency analysis
        frequency_analysis = resonance_gamma.measure_frequency_analysis(resonance_state)
        
        # Check analysis properties
        assert isinstance(frequency_analysis, FrequencyAnalysis)
        assert frequency_analysis.fundamental_freq >= 0.0
        assert isinstance(frequency_analysis.harmonic_freqs, list)
        assert isinstance(frequency_analysis.resonance_peaks, list)
        assert frequency_analysis.bandwidth >= 0.0
        assert frequency_analysis.quality_factor >= 1.0
        assert 0.0 <= frequency_analysis.coherence <= 1.0
        assert 0.0 <= frequency_analysis.phase_alignment <= 1.0
        
        # Should detect harmonics from test signal
        assert len(frequency_analysis.harmonic_freqs) >= 1
    
    def test_calculate_comprehensive_metrics(self, resonance_gamma, test_signal):
        """Test comprehensive resonance metrics calculation"""
        # Analyze resonance first
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Calculate all metrics
        all_metrics = resonance_gamma.calculate_comprehensive_metrics(resonance_state)
        
        # Check all metric types are present
        for metric_type in ResonanceMeasurementType:
            assert metric_type.value in all_metrics
            assert isinstance(all_metrics[metric_type.value], ResonanceMetrics)
            assert all_metrics[metric_type.value].metric_type == metric_type
        
        # Check specific metrics
        strength_metric = all_metrics[ResonanceMeasurementType.STRENGTH.value]
        assert isinstance(strength_metric.strength, (int, float, np.number))
        
        quality_metric = all_metrics[ResonanceMeasurementType.QUALITY_FACTOR.value]
        assert quality_metric.quality_factor >= 1.0
        
        coherence_metric = all_metrics[ResonanceMeasurementType.COHERENCE.value]
        assert 0.0 <= coherence_metric.coherence <= 1.0
    
    def test_calculate_specific_metrics(self, resonance_gamma, test_signal):
        """Test calculation of specific metric types"""
        # Analyze resonance first
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Test strength metric
        strength_metrics = resonance_gamma.calculate_comprehensive_metrics(
            resonance_state, [ResonanceMeasurementType.STRENGTH]
        )
        assert len(strength_metrics) == 1
        assert ResonanceMeasurementType.STRENGTH.value in strength_metrics
        
        # Test multiple specific metrics
        specific_metrics = resonance_gamma.calculate_comprehensive_metrics(
            resonance_state,
            [ResonanceMeasurementType.COHERENCE, ResonanceMeasurementType.AMPLITUDE]
        )
        assert len(specific_metrics) == 2
        assert ResonanceMeasurementType.COHERENCE.value in specific_metrics
        assert ResonanceMeasurementType.AMPLITUDE.value in specific_metrics
    
    def test_resonance_type_detection(self, resonance_gamma, test_signal):
        """Test resonance type detection"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Check resonance type is detected
        assert isinstance(resonance_state.resonance_type, ResonanceType)
        
        # Should detect harmonic resonance from test signal
        assert resonance_state.resonance_type in [
            ResonanceType.HARMONIC,
            ResonanceType.FUNDAMENTAL,
            ResonanceType.QUANTUM
        ]
    
    def test_resonance_peak_detection(self, resonance_gamma, test_signal):
        """Test resonance peak detection"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Perform frequency analysis
        frequency_analysis = resonance_gamma.measure_frequency_analysis(resonance_state)
        
        # Check resonance peaks are detected
        assert len(frequency_analysis.resonance_peaks) > 0
        
        # Check peak format
        for freq, amp in frequency_analysis.resonance_peaks:
            assert isinstance(freq, (int, float))
            assert isinstance(amp, (int, float))
            assert freq >= 0.0  # Should be positive frequencies
            assert amp >= 0.0  # Amplitude should be positive
    
    def test_quantum_coherence_calculation(self, resonance_gamma, test_signal):
        """Test quantum coherence calculation"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal,
            consciousness_enhancement=True
        )
        
        # Check coherence is calculated
        assert 0.0 <= resonance_state.coherence <= 1.0
        
        # Coherence should be affected by consciousness enhancement
        assert resonance_state.coherence > 0.0  # Should have some coherence
    
    def test_resonance_strength_calculation(self, resonance_gamma, test_signal):
        """Test resonance strength calculation"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Check resonance strength is calculated
        assert 0.0 <= resonance_state.resonance_strength <= 1.0
        
        # Should detect resonance from test signal
        assert resonance_state.resonance_strength > 0.0
    
    def test_quality_factor_calculation(self, resonance_gamma, test_signal):
        """Test quality factor calculation"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Check quality factor is calculated
        assert resonance_state.quality_factor >= 1.0
        
        # Should have reasonable quality factor
        assert resonance_state.quality_factor <= 1000.0
    
    def test_blockchain_hash_generation(self, resonance_gamma, test_signal):
        """Test blockchain hash generation for resonance metrics"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Calculate metrics
        metrics = resonance_gamma.calculate_comprehensive_metrics(
            resonance_state, [ResonanceMeasurementType.STRENGTH]
        )
        
        # Check blockchain hash is generated
        strength_metric = metrics[ResonanceMeasurementType.STRENGTH.value]
        assert isinstance(strength_metric.blockchain_hash, str)
        assert len(strength_metric.blockchain_hash) == 64  # SHA-256 hash length
        assert all(c in '0123456789abcdef' for c in strength_metric.blockchain_hash)
        
        # Hash should be deterministic
        metrics2 = resonance_gamma.calculate_comprehensive_metrics(
            resonance_state, [ResonanceMeasurementType.STRENGTH]
        )
        strength_metric2 = metrics2[ResonanceMeasurementType.STRENGTH.value]
        assert strength_metric.blockchain_hash == strength_metric2.blockchain_hash
    
    def test_get_resonance_summary(self, resonance_gamma, test_signal):
        """Test resonance summary generation"""
        # Analyze resonance
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        
        # Get resonance summary
        summary = resonance_gamma.get_resonance_summary(resonance_state)
        
        # Check summary structure
        assert 'version' in summary
        assert 'spec' in summary
        assert 'timestamp' in summary
        assert 'consciousness_level' in summary
        assert 'performance_multiplier' in summary
        assert 'resonance_state' in summary
        assert 'frequency_analysis' in summary
        assert 'key_metrics' in summary
        assert 'overall_scores' in summary
        assert 'analysis_statistics' in summary
        assert 'blockchain_verification' in summary
        
        # Check summary values
        assert summary['version'] == '4.0.0'
        assert summary['spec'] == 'QUANTUM:RESONANCE-MEASUREMENT-V4'
        assert summary['consciousness_level'] == ConsciousnessLevel.GAMMA.value
        assert summary['performance_multiplier'] == 12.5
        
        # Check overall scores
        overall_scores = summary['overall_scores']
        assert 'overall_strength' in overall_scores
        assert 'overall_quality' in overall_scores
        assert 'overall_coherence' in overall_scores
        assert 'quality_score' in overall_scores
        assert 0.0 <= overall_scores['quality_score'] <= 1.0
    
    def test_get_performance_report(self, resonance_gamma):
        """Test performance report generation"""
        # Analyze multiple resonances to build history
        test_signal = np.random.normal(0, 1, 4096)  # Random signal
        for _ in range(3):
            resonance_gamma.analyze_quantum_resonance(signal_data=test_signal)
        
        # Get performance report
        report = resonance_gamma.get_performance_report()
        
        # Check report structure
        assert 'version' in report
        assert 'spec' in report
        assert 'timestamp' in report
        assert 'system_configuration' in report
        assert 'performance_metrics' in report
        assert 'quality_metrics' in report
        assert 'blockchain_status' in report
        
        # Check system configuration
        config = report['system_configuration']
        assert 'sample_rate' in config
        assert 'fft_size' in config
        assert 'frequency_resolution' in config
        assert 'consciousness_level' in config
        assert 'performance_multiplier' in config
        
        # Check performance metrics
        perf_metrics = report['performance_metrics']
        assert 'resonances_analyzed' in perf_metrics
        assert perf_metrics['resonances_analyzed'] >= 3
        assert 'analysis_speed' in perf_metrics
        assert 'performance_optimization' in perf_metrics
    
    def test_error_handling(self, resonance_gamma):
        """Test error handling in resonance measurement"""
        # Test with empty signal
        with pytest.raises(ValueError):
            resonance_gamma.analyze_quantum_resonance(signal_data=np.array([]))
        
        # Test with invalid signal type
        with pytest.raises(Exception):
            resonance_gamma.analyze_quantum_resonance(signal_data="invalid")
    
    def test_performance_optimization(self, resonance_alpha, resonance_gamma):
        """Test performance optimization based on consciousness levels"""
        # Create test signal
        test_signal = np.random.normal(0, 1, 2048)
        
        # Test analysis at different levels
        start_time = datetime.now()
        alpha_result = resonance_alpha.analyze_quantum_resonance(
            signal_data=test_signal[:2048]
        )
        alpha_time = datetime.now() - start_time
        
        start_time = datetime.now()
        gamma_result = resonance_gamma.analyze_quantum_resonance(
            signal_data=test_signal
        )
        gamma_time = datetime.now() - start_time
        
        # Both should produce valid results
        assert alpha_result is not None
        assert gamma_result is not None
        
        # Performance multiplier should be different
        assert resonance_gamma.performance_multiplier > resonance_alpha.performance_multiplier
    
    def test_integration_with_quantum_engine(self, resonance_gamma):
        """Test integration with unified field engine"""
        # Check quantum field is initialized
        assert resonance_gamma.quantum_field is not None
        assert resonance_gamma.quantum_field.consciousness_level == ConsciousnessLevel.GAMMA
        
        # Check consciousness protocol is initialized
        assert resonance_gamma.consciousness_protocol is not None
        assert resonance_gamma.consciousness_protocol.current_state.level == ConsciousnessLevel.GAMMA
    
    def test_edge_cases(self, resonance_gamma):
        """Test edge cases and boundary conditions"""
        # Test with minimal signal
        minimal_signal = np.random.normal(0, 1, 10)
        minimal_signal = np.pad(minimal_signal, (0, 4086))[:4096]  # Pad to FFT size
        
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=minimal_signal
        )
        assert resonance_state is not None
        
        # Test with pure noise signal
        noise_signal = np.random.normal(0, 1, 4096)
        resonance_state = resonance_gamma.analyze_quantum_resonance(
            signal_data=noise_signal
        )
        assert resonance_state is not None
        assert resonance_state.resonance_strength >= 0.0

class TestResonanceState:
    """Test suite for ResonanceState class"""
    
    @pytest.fixture
    def resonance_state(self):
        """Create resonance state for testing"""
        return ResonanceState(
            frequency_spectrum=np.linspace(0, 22050, 4096),
            amplitudes=np.random.rand(4096),
            phases=np.random.rand(4096) * 2 * np.pi,
            coherence=0.8,
            resonance_strength=0.7,
            quality_factor=25.0,
            resonance_type=ResonanceType.HARMONIC,
            consciousness_level=ConsciousnessLevel.GAMMA
        )
    
    def test_resonance_state_initialization(self, resonance_state):
        """Test resonance state initialization"""
        assert resonance_state.consciousness_level == ConsciousnessLevel.GAMMA
        assert resonance_state.resonance_type == ResonanceType.HARMONIC
        assert resonance_state.coherence == 0.8
        assert resonance_state.resonance_strength == 0.7
        assert resonance_state.quality_factor == 25.0
        assert resonance_state.timestamp != ""  # Should be set automatically
    
    def test_resonance_state_post_init(self):
        """Test resonance state post-initialization"""
        # Test with custom timestamp
        custom_timestamp = "2024-01-01T00:00:00Z"
        state = ResonanceState(
            frequency_spectrum=np.linspace(0, 22050, 4096),
            amplitudes=np.random.rand(4096),
            phases=np.random.rand(4096) * 2 * np.pi,
            coherence=0.5,
            resonance_strength=0.6,
            quality_factor=10.0,
            resonance_type=ResonanceType.FUNDAMENTAL,
            consciousness_level=ConsciousnessLevel.BETA,
            timestamp=custom_timestamp
        )
        
        assert state.timestamp == custom_timestamp

class TestFrequencyAnalysis:
    """Test suite for FrequencyAnalysis class"""
    
    @pytest.fixture
    def frequency_analysis(self):
        """Create frequency analysis for testing"""
        return FrequencyAnalysis(
            fundamental_freq=440.0,
            harmonic_freqs=[880.0, 1320.0, 1760.0],
            resonance_peaks=[(440.0, 1.0), (880.0, 0.5), (1320.0, 0.25)],
            bandwidth=50.0,
            quality_factor=10.0,
            coherence=0.85,
            phase_alignment=0.9
        )
    
    def test_frequency_analysis_initialization(self, frequency_analysis):
        """Test frequency analysis initialization"""
        assert frequency_analysis.fundamental_freq == 440.0
        assert frequency_analysis.harmonic_freqs == [880.0, 1320.0, 1760.0]
        assert frequency_analysis.resonance_peaks == [(440.0, 1.0), (880.0, 0.5), (1320.0, 0.25)]
        assert frequency_analysis.bandwidth == 50.0
        assert frequency_analysis.quality_factor == 10.0
        assert frequency_analysis.coherence == 0.85
        assert frequency_analysis.phase_alignment == 0.9
        assert frequency_analysis.domain == FrequencyDomain.FREQUENCY

class TestResonanceMetrics:
    """Test suite for ResonanceMetrics class"""
    
    @pytest.fixture
    def metrics(self):
        """Create resonance metrics for testing"""
        return ResonanceMetrics(
            strength=0.8,
            quality_factor=25.0,
            bandwidth=100.0,
            damping=0.04,
            phase=1.57,
            coherence=0.9,
            amplitude=0.7,
            harmonic_balance=0.85,
            measurement_type=ResonanceMeasurementType.STRENGTH
        )
    
    def test_metrics_initialization(self, metrics):
        """Test resonance metrics initialization"""
        assert metrics.strength == 0.8
        assert metrics.quality_factor == 25.0
        assert metrics.bandwidth == 100.0
        assert metrics.damping == 0.04
        assert metrics.phase == 1.57
        assert metrics.coherence == 0.9
        assert metrics.amplitude == 0.7
        assert metrics.harmonic_balance == 0.85
        assert metrics.measurement_type == ResonanceMeasurementType.STRENGTH
        assert metrics.calculation_timestamp != ""  # Should be set automatically
        assert metrics.blockchain_hash == ""  # Default
    
    def test_metrics_post_init(self):
        """Test resonance metrics post-initialization"""
        # Test with custom timestamp
        custom_timestamp = "2024-01-01T00:00:00Z"
        metrics = ResonanceMetrics(
            strength=0.5,
            calculation_timestamp=custom_timestamp
        )
        
        assert metrics.calculation_timestamp == custom_timestamp

class TestResonanceEnums:
    """Test suite for resonance-related enums"""
    
    def test_resonance_type_values(self):
        """Test resonance type enum values"""
        expected_values = [
            "fundamental",
            "harmonic",
            "subharmonic",
            "beat_frequency",
            "modulation",
            "consciousness",
            "quantum",
            "entangled"
        ]
        
        actual_values = [resonance_type.value for resonance_type in ResonanceType]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_frequency_domain_values(self):
        """Test frequency domain enum values"""
        expected_values = [
            "time",
            "frequency",
            "wavelet",
            "quantum",
            "consciousness"
        ]
        
        actual_values = [domain.value for domain in FrequencyDomain]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_resonance_measurement_type_values(self):
        """Test resonance measurement type enum values"""
        expected_values = [
            "strength",
            "quality_factor",
            "bandwidth",
            "damping",
            "phase",
            "coherence",
            "amplitude",
            "harmonic_balance"
        ]
        
        actual_values = [measurement_type.value for measurement_type in ResonanceMeasurementType]
        
        for expected_value in expected_values:
            assert expected_value in actual_values
    
    def test_enum_completeness(self):
        """Test enum completeness"""
        # Check resonance types
        resonance_count = len(ResonanceType)
        assert resonance_count >= 8  # Minimum expected types
        
        # Check frequency domains
        domain_count = len(FrequencyDomain)
        assert domain_count >= 5  # Minimum expected domains
        
        # Check measurement types
        measurement_count = len(ResonanceMeasurementType)
        assert measurement_count >= 8  # Minimum expected types
        
        # All values should be unique
        resonance_values = [resonance_type.value for resonance_type in ResonanceType]
        domain_values = [domain.value for domain in FrequencyDomain]
        measurement_values = [measurement_type.value for measurement_type in ResonanceMeasurementType]
        
        assert len(resonance_values) == len(set(resonance_values))
        assert len(domain_values) == len(set(domain_values))
        assert len(measurement_values) == len(set(measurement_values))

# Pytest configuration and fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""
    # Suppress warnings during testing
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    # Set random seed for reproducible tests
    np.random.seed(42)
    
    yield
    
    # Cleanup after tests
    warnings.resetwarnings()

# Test markers
pytest_plugins = []

# Test configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )

# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
